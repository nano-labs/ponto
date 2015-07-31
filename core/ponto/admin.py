# -*- encoding: utf-8 -*-
"""Admin (Duh!)."""

from math import sqrt
from datetime import timedelta

from django.contrib import admin
from django.shortcuts import render

from ponto.models import Entrada
from ponto.views import relatorio


class EntradaAdmin(admin.ModelAdmin):

    list_display = ['usuario', 'dia', 'entrada', 'saida_almoco',
                    'volta_almoco', 'saida', 'tipo', 'has_foto']
    list_filter = ['tipo', 'usuario']
    search_fields = ('usuario', 'comentário')

admin.site.register(Entrada, EntradaAdmin)
