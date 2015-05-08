# -*- encoding: utf-8 -*-

from datetime import timedelta

from django.contrib import admin
from django.shortcuts import render

from ponto.models import Entrada

admin.site.disable_action('delete_selected')

class PontoAdmin(admin.ModelAdmin):
    list_display = ['dia', 'entrada', 'saida_almoco', 'volta_almoco', 'saida', 'total', 'extra', 'deficit', 'folga', 'abonado', 'comentario_curto', 'has_foto']
    list_filter = ['abonado', 'folga', 'usuario']
    search_fields = ('usuario', 'comentário')
    actions = ['make_relatorio']
    exclude = ['usuario']

    def make_relatorio(self, request, queryset):
        total_extra = timedelta(0)
        total_deficit = timedelta(0)
        total_trabalhado = timedelta(0)
        total_alvo = timedelta(0)

        entradas = []
        inicio = queryset.last()
        fim = queryset.first()
        total_dias = (fim.dia - inicio.dia).days
        for i in range(total_dias + 1):
            dia = inicio.dia + timedelta(days=i)
            if dia.isoweekday() in [6, 7]:  # FIM DE SEMANA
                entrada = Entrada(dia=dia, entrada=None)
                entrada.fim_de_semana = True
            else:
                entrada = Entrada.objects.get_or_none(dia=dia)
                if not entrada:
                    entrada = Entrada(dia=dia, entrada=None)
                    entrada.inexistente = True
            total_extra = entrada.extra + total_extra if entrada.extra else total_extra
            total_deficit = entrada.deficit + total_deficit if entrada.deficit else total_deficit
            total_trabalhado = total_trabalhado + entrada.total if entrada.total else total_trabalhado
            total_alvo = total_alvo + entrada.total_alvo if entrada.util else total_alvo
            entradas.append(entrada)

        saldo = total_extra - total_deficit
        saldo_string = Entrada.format_time(saldo)  # "%02d:%02d:00" % (int(saldo.total_seconds()/60/60), int((abs(saldo.total_seconds()) - abs(int(saldo.total_seconds()/60/60)*60*60))/60) )
        context = {'entradas': entradas,
                   'total_extra': total_extra,
                   'total_deficit': total_deficit,
                   'saldo': saldo,
                   'saldo_string': saldo_string,
                   'total_trabalhado': Entrada.format_time(total_trabalhado),
                   'total_alvo': Entrada.format_time(total_alvo)}
        return render(request, "relatorio.html", context)
    make_relatorio.short_description = u"Gerar relatório"

    def has_delete_permission(self, *args, **kwargs):
        return False

    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        return super(PontoAdmin, self).save_model(request, obj, form, change)

admin.site.register(Entrada, PontoAdmin)