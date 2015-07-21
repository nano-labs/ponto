# -*- encoding: utf-8 -*-
u"""E isso é um model."""
from datetime import datetime, date, timedelta

from django.db import models
from django.contrib.auth.models import User

from utils.models import BaseModel

TOTAL_DIA = timedelta(hours=8)


class Entrada(BaseModel):

    u"""Tá tudo aqui."""

    usuario = models.ForeignKey(User, verbose_name=u"Funcionario")
    dia = models.DateField(u'Dia', default=datetime.today())
    entrada = models.DateTimeField(u'Entrada', blank=True, null=True,
                                   default=datetime.today())
    saida_almoco = models.DateTimeField(u'Saída para almoço', blank=True,
                                        null=True)
    volta_almoco = models.DateTimeField(u'Volta do almoço', blank=True,
                                        null=True)
    saida = models.DateTimeField(u'Saída', blank=True, null=True)
    foto = models.ImageField(upload_to='fotos', null=True, blank=True,
                                       verbose_name=u"Foto do ticket")
    comentario = models.TextField(u'Comentário', blank=True, null=True)

    folga = models.BooleanField(u'Folga ou feriado', default=False)
    abonado = models.BooleanField(u'Falta abonada', default=False)

    fim_de_semana = False
    inexistente = False

    total_alvo = TOTAL_DIA

    def __unicode__(self):
        """Unicode."""
        return u'%s' % self.dia.strftime("%d/%m/%Y")

    @classmethod
    def format_time(cls, delta):
        """Formata um timedelta object em string."""
        n = ''
        if delta.total_seconds() < 0:
            n = '-'
        return "%s%02d:%02d" % (n, int(delta.total_seconds()/60/60),
                                int((abs(delta.total_seconds()) -
                                    abs(int(delta.total_seconds()/60/60)*60*60))/60) )

    @property
    def total(self):
        """Caucula o tempo total de trabalho deste dia."""
        if self.dia == datetime.today():
            if all([self.entrada, self.saida_almoco, self.volta_almoco,
                    self.saida]):
                return (self.saida - self.entrada) - (self.volta_almoco -
                                                       self.saida_almoco)
            elif all([self.entrada, self.saida_almoco, self.volta_almoco]):
                tempo = datetime.now() - self.entrada
                almoco = self.volta_almoco - self.saida_almoco
                return tempo - almoco
            elif all([self.entrada, self.saida_almoco]):
                return self.saida_almoco - self.entrada
            elif self.entrada:
                return datetime.now() - self.entrada
            else:
                return u""

        if all([self.entrada, self.saida_almoco, self.volta_almoco,
                self.saida]):
            return (self.saida - self.entrada) - (self.volta_almoco -
                                                  self.saida_almoco)
        elif self.entrada and self.saida:
            return self.saida - self.entrada
        elif self.dia == datetime.today():
            if self.entrada and self.saida_almoco and self.volta_almoco:
                return (self.saida - datetime.now()) - (self.volta_almoco -
                                                      self.saida_almoco)
            elif self.entrada:
                return datetime.now() - self.entrada
        else:
            return u""

    @property
    def total_horas(self):
        """Caucula o tempo total em minutos de trabalho deste dia."""
        t = self.total
        if t == "":
            return 0
        return t.total_seconds() / 60.0 / 60.0

    @property
    def total_horas_str(self):
        """Caucula o tempo total em minutos de trabalho deste dia."""
        return ("%.2f" % self.total_horas).replace(",", ".")

    @property
    def ate_agora(self):
        u"""Retorna a string de tempo trabalhando ate agora."""
        if all([self.entrada, self.saida_almoco, self.volta_almoco,
                self.saida]):
            tempo = (self.saida - self.entrada) - (self.volta_almoco -
                                                   self.saida_almoco)
        elif all([self.entrada, self.saida_almoco, self.volta_almoco]):
            tempo = datetime.now() - self.entrada
            almoco = self.volta_almoco - self.saida_almoco
            tempo = tempo - almoco
        elif all([self.entrada, self.saida_almoco]):
            tempo = self.saida_almoco - self.entrada
        elif self.entrada:
            tempo = datetime.now() - self.entrada
        else:
            return "Nada!"
        horas = int(tempo.total_seconds() / 60 / 60)
        minutos = int((tempo.total_seconds() / 60) - (horas * 60))
        return "%s horas e %s minutos" % (horas, minutos)

    @property
    def extra(self):
        """Calcula o total de horas extras do dia."""
        if self.folga or self.abonado:
            return timedelta(minutes=0)
        if self.total:
            if self.total > TOTAL_DIA:
                return self.total - TOTAL_DIA
        return u""

    @property
    def deficit(self):
        """Calcula o tempo faltoso deste dia."""
        if self.folga or self.abonado:
            return timedelta(minutes=0)
        if self.total:
            if self.total < TOTAL_DIA:
                return TOTAL_DIA - self.total
        return u""

    @property
    def comentario_curto(self):
        """Precisa explciar?."""
        if self.comentario:
            return u''.join(self.comentario[:50])
        elif self.folga:
            return u'Folga ou feriado'
        return u""

    @property
    def minutos_hoje(self):
        u"""Gambiarra. Acho que nem uso mais. Não tente entender."""
        def calcula_minutos(tempo):
            # print tempo
            t = 'null'
            if tempo:
                t = (tempo.hour * 60) + tempo.minute
            return t

        r =  {'entrada': {'label': self.entrada.strftime("%H:%M") if self.entrada else 'null',
                          'minutos': calcula_minutos(self.entrada)},
              'saida': {'label': self.saida.strftime("%H:%M") if self.saida else 'null',
                        'minutos': calcula_minutos(self.saida)}}
        return r

    @property
    def util(self):
        u"""Retorna se é um dia útil nou não."""
        return not any([self.folga, self.abonado, self.fim_de_semana])

    def has_foto(self):
        """Ok..."""
        if self.foto:
            return True
        return False
    has_foto.boolean = True
    has_foto.short_description = "Imagem"

    class Meta:
        unique_together = (('usuario', 'dia'), )
        ordering = ('-dia',)
        verbose_name = u'Entrada'
        verbose_name_plural = u'Entrada'


class EntradaTodos(Entrada):

    class Meta:
        proxy = True
