# -*- encoding: utf-8 -*-
"""Admin (Duh!)."""

from math import sqrt
from datetime import timedelta

from django.contrib import admin
from django.shortcuts import render

from ponto.models import Entrada, EntradaTodos
from ponto.views import relatorio

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

        id_inicio = queryset.last().id
        id_fim = queryset.first().id

        return relatorio(request, id_inicio, id_fim)
    make_relatorio.short_description = u"Gerar relatório"

    def has_delete_permission(self, *args, **kwargs):
        u"""Ninguém apagua porra nenhuma nessa merda!."""
        return False

    def save_model(self, request, obj, form, change):
        u"""Automáticamente associa o usuário logado à entrada."""
        obj.usuario = request.user
        return super(PontoAdmin, self).save_model(request, obj, form, change)


class EntradaTodosAdmin(admin.ModelAdmin):

    list_display = ['usuario', 'dia', 'entrada', 'saida_almoco', 'volta_almoco',
                    'saida', 'tipo', 'has_foto']
    exclude = []

    # def save_model(self, request, obj, form, change):
    #     return super(PontoAdmin, self).save_model(request, obj, form, change)

    # def get_queryset(self, request):
    #     u"""Retorna o queryset padrão usado no admin."""
    #     return super(admin.ModelAdmin, self).get_queryset(request)

    # def has_delete_permission(self, *args, **kwargs):
    #     return True

admin.site.register(Entrada)#, PontoAdmin)
admin.site.register(EntradaTodos, EntradaTodosAdmin)
