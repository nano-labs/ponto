# -*- encoding: utf-8 -*-
"""Admin (Duh!)."""

from math import sqrt
from datetime import timedelta

from django.contrib import admin
from django.shortcuts import render

from ponto.models import Entrada

admin.site.disable_action('delete_selected')


class PontoAdmin(admin.ModelAdmin):

    """Admin com basicamente tudo dentro."""

    list_display = ['dia', 'entrada', 'saida_almoco', 'volta_almoco',
                    'saida', 'total', 'extra', 'deficit', 'folga',
                    'abonado', 'comentario_curto', 'has_foto']
    list_filter = ['abonado', 'folga', 'usuario']
    search_fields = ('usuario', 'comentário')
    actions = ['make_relatorio']
    exclude = ['usuario']

    def get_queryset(self, request):
        u"""Retorna o queryset padrão usado no admin."""
        qs = super(PontoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)

    def make_relatorio(self, request, queryset):
        u"""Action que gera o relatório."""
        def calcula_media(l):
            l = [i for i in l if i is not 'null']
            minutos = sum(l) / float(len(l))
            dp = sqrt((sum([i ** 2 for i in l]) - ((sum(l) ** 2) / len(l))) / (len(l) - 1))
            minutos = int(minutos)
            hora = minutos / 60
            minuto = minutos - (hora * 60)
            return minutos, dp, u'%02d:%02d (σ = %d min)' % (hora, minuto, int(dp))

        total_extra = timedelta(0)
        total_deficit = timedelta(0)
        total_trabalhado = timedelta(0)
        total_alvo = timedelta(0)
        entrada_minutos = []
        saida_minutos = []

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
            entrada_minutos.append(entrada.minutos_hoje['entrada']['minutos'])
            saida_minutos.append(entrada.minutos_hoje['saida']['minutos'])

        saldo = total_extra - total_deficit
        saldo_string = Entrada.format_time(saldo)  # "%02d:%02d:00" % (int(saldo.total_seconds()/60/60), int((abs(saldo.total_seconds()) - abs(int(saldo.total_seconds()/60/60)*60*60))/60) )
        context = {'entradas': entradas,
                   'total_extra': total_extra,
                   'total_deficit': total_deficit,
                   'saldo': saldo,
                   'saldo_string': saldo_string,
                   'total_trabalhado': Entrada.format_time(total_trabalhado),
                   'total_alvo': Entrada.format_time(total_alvo),
                   'saida_media': calcula_media(saida_minutos),
                   'entrada_media': calcula_media(entrada_minutos)}
        return render(request, "relatorio.html", context)
    make_relatorio.short_description = u"Gerar relatório"

    def has_delete_permission(self, *args, **kwargs):
        u"""Ninguém apagua porra nenhuma nessa merda!."""
        return False

    def save_model(self, request, obj, form, change):
        u"""Automáticamente associa o usuário logado à entrada."""
        obj.usuario = request.user
        return super(PontoAdmin, self).save_model(request, obj, form, change)

admin.site.register(Entrada, PontoAdmin)