# -*- encoding: utf-8 -*-
u"""Views."""

from datetime import datetime, timedelta
from math import sqrt

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.http import Http404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.safestring import mark_safe
from ponto.models import Entrada

@staff_member_required
def home(request):
    usuario = request.user
    agora = datetime.now()
    entrada = Entrada.objects.get_or_none(usuario=usuario, dia=datetime.today())
    context = {"entrada": entrada,
               "agora": agora,
               "usuario": usuario}
    if Entrada.objects.filter(usuario=usuario).count() >= 2:
        trinta_dias = datetime.today() - timedelta(31)
        id_inicio = Entrada.objects.filter(usuario=usuario, dia__gte=trinta_dias).last().id
        id_fim = Entrada.objects.filter(usuario=usuario).first().id
        rel = cria_relatorio(id_inicio, id_fim, usuario)
        context.update(rel)
    return render(request, "home.html", context)

@staff_member_required
def registrar(request, momento):
    usuario = request.user
    entrada = Entrada.objects.get_or_none(usuario=usuario, dia=datetime.today())
    if not entrada:
        entrada = Entrada(usuario=usuario, dia=datetime.today())

    agora = datetime.now()

    if momento == "entrada":
        agora = datetime.now() - timedelta(minutes=10)
        entrada.entrada = agora
    elif momento == "saida_almoco":
        entrada.saida_almoco = agora
    elif momento == "volta_almoco":
        entrada.volta_almoco = agora
    elif momento == "saida":
        entrada.saida = agora
    else:
        raise Http404
    entrada.save()
    messages.add_message(request, messages.INFO, 'Ponto registrado em %s' % agora)
    if request.GET.get('device') == 'ios':
        return redirect('ios_home')
    return redirect('home')

def cria_relatorio(id_inicio, id_fim, usuario):
    u"""Action que gera o relatório."""
    def calcula_media(l):
        l = [i for i in l if i is not 'null']
        minutos = 0
        dp = 0
        if len(l) >= 2:
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
    inicio = Entrada.objects.get(id=id_inicio)
    fim = Entrada.objects.get(id=id_fim)
    total_dias = (fim.dia - inicio.dia).days
    for i in range(total_dias + 1):
        dia = inicio.dia + timedelta(days=i)
        if dia.isoweekday() in [6, 7]:  # FIM DE SEMANA
            entrada = Entrada(dia=dia, entrada=None, usuario=usuario)
            entrada.fim_de_semana = True
        else:
            entrada = Entrada.objects.get_or_none(dia=dia, usuario=usuario)
            if not entrada:
                entrada = Entrada(dia=dia, entrada=None, usuario=usuario)
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
    return context


def relatorio(request, id_inicio, id_fim):
    u"""Action que gera o relatório."""
    context = cria_relatorio(id_inicio, id_fim, request.user)
    return render(request, "relatorio.html", context)

def ios_login(request):
    if request.user.is_authenticated():
        return redirect('ios_home')

    context = RequestContext(request)
    logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('ios_home')
        context["falha_autenticacao"] = True
    return render_to_response('ios_login.html', context_instance=context)

def ios_logout(request):
    logout(request)
    return redirect('ios_login')

@staff_member_required
def ios_home(request):
    usuario = request.user
    agora = datetime.now()
    entrada = Entrada.objects.get_or_none(usuario=usuario, dia=datetime.today())
    context = {"entrada": entrada,
               "agora": agora,
               "usuario": usuario}
    if Entrada.objects.filter(usuario=usuario).count() >= 2:
        trinta_dias = datetime.today() - timedelta(31)
        id_inicio = Entrada.objects.filter(usuario=usuario, dia__gte=trinta_dias).last().id
        id_fim = Entrada.objects.filter(usuario=usuario).first().id
        rel = cria_relatorio(id_inicio, id_fim, usuario)
        context.update(rel)
    return render(request, "ios_home.html", context)

# @staff_member_required
def ios_relatorio(request):
    usuario = request.user
    inicio = datetime.today() - timedelta(days=30)
    entradas = Entrada.objects.filter(usuario=usuario, dia__gte=inicio).order_by('dia')

    saldo = 0
    for e in Entrada.objects.filter(dia__lt=inicio).order_by('dia'):
        saldo += (e.total_horas - 8.0)
    saldo_graf = []
    for e in entradas:
        saldo += (e.total_horas - 8.0)
        saldo_graf.append({"dia": e.dia, "saldo": saldo})


    context = {"entradas": entradas, "saldos": saldo_graf}
    return render(request, "ios_relatorio.html", context)

