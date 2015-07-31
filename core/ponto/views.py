# -*- encoding: utf-8 -*-
u"""Views."""

from datetime import datetime, timedelta
from math import sqrt

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
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
    usuarios = []
    if usuario.is_superuser:
        user_id = request.GET.get('usuario')
        if user_id:
            usuario = User.objects.get(id=user_id)
        for u in User.objects.filter(is_superuser=False):
            ud = {'entrada': Entrada.objects.get_or_none(usuario=u,
                                            dia=datetime.today()),
                  'saldo': 10,
                  'usuario': u}
            usuarios.append(ud)

    agora = datetime.now()
    entrada = Entrada.objects.get_or_none(usuario=usuario, dia=datetime.today())
    context = {"entrada": entrada,
               "agora": agora,
               "usuario": usuario,
               "usuarios": usuarios}
    if Entrada.objects.filter(usuario=usuario).count() >= 2:
        primeiro_dia = Entrada.objects.filter(usuario=usuario).last().dia
        primeiro_dia = datetime(*primeiro_dia.timetuple()[:6])
        dias = (datetime.today() - primeiro_dia).total_seconds() / 86400
        dias = [[(primeiro_dia + timedelta(i)).strftime("%d/%m/%Y"),
                 (primeiro_dia + timedelta(i)).strftime("%Y-%m-%d")]
                for i in xrange(int(dias) + 1)]
        context['lista_dias'] = dias
        data_inicio = request.GET.get('inicio',
                                      (datetime.today() - timedelta(30)).strftime("%Y-%m-%d"))
        data_fim = request.GET.get('fim',
                                   datetime.today().strftime("%Y-%m-%d"))
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d")
        if data_inicio > data_fim:
            data_inicio = data_fim - timedelta(1)
        inicio = Entrada.objects.filter(usuario=usuario,
                                        dia__gte=data_inicio).last()
        fim = Entrada.objects.filter(usuario=usuario,
                                     dia__lte=data_fim).first()
        if inicio and fim:
            id_inicio = inicio.id
            id_fim = fim.id
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
        u"""Retorna a média e desvio padrão."""
        l = list(l)
        l = [i for i in l if i]
        minutos = 0
        dp = 0
        if len(l) >= 2:
            minutos = sum(l) / float(len(l))
            dp = sqrt((sum([i ** 2 for i in l]) - ((sum(l) ** 2) / len(l))) / (len(l) - 1))
        minutos = int(minutos)
        hora = minutos / 60
        minuto = minutos - (hora * 60)
        return minutos, dp, u'%02d:%02d (σ = %d min)' % (hora, minuto, int(dp))

    entradas = []
    inicio = Entrada.objects.get(id=id_inicio)
    saldo_inicial = inicio.saldo_ate_hoje()
    fim = Entrada.objects.get(id=id_fim)
    total_dias = (fim.dia - inicio.dia).days
    saldo_periodo = timedelta(0)
    trabalhado = timedelta(0)
    desejado = timedelta(0)
    medias = []
    for i in range(total_dias + 1):
        dia = inicio.dia + timedelta(days=i)
        e = Entrada.objects.get_or_none(dia=dia, usuario=usuario)
        if not e:
            e = Entrada(dia=dia, usuario=usuario)
        entradas.append(e)
        saldo_periodo += e.saldo
        trabalhado += e.total
        desejado += e.desejado
        medias.append(e.minutos())

    media_entrada, media_saida, media_almoco = [calcula_media(l) for l in zip(*medias)]
    eficiencia = 100.0
    if desejado.total_seconds() > 0:
        eficiencia = trabalhado.total_seconds() / desejado.total_seconds() * 100.0

    tmp_saldo = saldo_inicial
    saldo_graf = []
    for e in entradas:
        if e.util:
            tmp_saldo += e.saldo
            horas = ("%.2f" % (tmp_saldo.total_seconds() / 60 / 60)).replace(",", ".")
            saldo_graf.append(horas)

    context = {"entradas": entradas,
               "inicio": inicio,
               "fim": fim,
               "medias": {"entrada": media_entrada[2],
                          "saida": media_saida[2],
                          "almoco": media_almoco[2]},
               "trabalhado": Entrada.delta_to_string(trabalhado),
               "desejado": Entrada.delta_to_string(desejado),
               "eficiencia": "%.2f%%" % eficiencia,
               "saldo_graf": saldo_graf,
               "saldo_periodo": Entrada.delta_to_html(saldo_periodo),
               "saldo_total": Entrada.delta_to_html(saldo_inicial + saldo_periodo)}
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
        id_inicio = Entrada.objects.filter(usuario=usuario).last().id
        id_fim = Entrada.objects.filter(usuario=usuario).first().id
        rel = cria_relatorio(id_inicio, id_fim, usuario)
        context.update(rel)
        trinta_dias = datetime.today() - timedelta(31)
        id_inicio = Entrada.objects.filter(usuario=usuario, dia__gte=trinta_dias).last().id
        id_fim = Entrada.objects.filter(usuario=usuario).first().id
        rel = cria_relatorio(id_inicio, id_fim, usuario)
        context['30_dias'] = rel
    return render(request, "ios_home.html", context)


@staff_member_required
def ios_relatorio(request):
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
    return render(request, "ios_relatorio.html", context)
