# -*- encoding: utf-8 -*-
u"""E isso é um model."""
from datetime import datetime, date, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from utils.models import BaseModel

TOTAL_DIA = timedelta(hours=8)


class Entrada(BaseModel):

    u"""Tá tudo aqui."""

    TIPOS = (('util', u"Dia útil"),
             ('falta', u"Falta"),
             ('folga', u"Folga ou feriado"),
             ('abonado', u"Falta abonada"),
             ('consumo', u"Consumo de hora extra"))

    usuario = models.ForeignKey(User, verbose_name=u"Funcionario")
    dia = models.DateField(u'Dia', default=datetime.today())
    entrada = models.DateTimeField(u'Entrada', blank=True, null=True)
    saida_almoco = models.DateTimeField(u'Saída para almoço', blank=True,
                                        null=True)
    volta_almoco = models.DateTimeField(u'Volta do almoço', blank=True,
                                        null=True)
    saida = models.DateTimeField(u'Saída', blank=True, null=True)
    foto = models.ImageField(upload_to='fotos', null=True, blank=True,
                                       verbose_name=u"Foto do ticket")
    comentario = models.TextField(u'Comentário', blank=True, null=True)
    tipo = models.CharField(u"Tipo", max_length=20, choices=TIPOS,
                            default='util', blank=False, null=False)

    def __unicode__(self):
        """Unicode."""
        return u'%s' % self.dia.strftime("%d/%m/%Y")

    def is_weekend(self, dia=None):
        u"""Informa se o dia é um fim de semana."""
        dia = dia or self.dia
        if dia.weekday() in [5, 6]:
            return True
        return False

    @property
    def util(self):
        u"""Informa se é um dia útil."""
        if self.is_weekend() or self.tipo in ['folga', 'abonado']:
            return False
        return True    

    @property
    def almoco(self):
        u"""Tempo utilizado no almoço."""
        if self.saida_almoco and self.volta_almoco:
            return self.volta_almoco - self.saida_almoco
        elif self.saida_almoco and self.dia == datetime.today():
            return datetime.now() - self.saida_almoco
        return timedelta(0)

    @property
    def total(self):
        u"""Tempo total trabalhado no dia."""
        if self.tipo in ['consumo', 'falta']:
            return timedelta(0)
        if self.entrada:
            if self.saida:
                return self.saida - self.entrada - self.almoco
            elif self.dia.strftime("%d/%m/%Y") == datetime.today().strftime("%d/%m/%Y"):
                return datetime.now() - self.entrada - self.almoco
        return timedelta(0)

    @property
    def desejado(self):
        u"""Retorna o tempo de trabalho desejado para hoje."""
        if not self.util:
            return timedelta(0)
        return TOTAL_DIA

    @classmethod
    def delta_to_string(cls, delta):
        u"""Transforma um timedelta numa string no formato [-]HH:MM:SS."""
        segundos = int(delta.total_seconds())
        sinal = "" if segundos >= 0 else "-"
        segundos = abs(segundos)
        horas = segundos / 60 / 60
        minutos = (segundos - (horas * 60 * 60)) / 60
        # segundos = segundos - (minutos * 60) - (horas * 60 * 60)
        return "%s%02d:%02d" % (sinal, horas, minutos)

    @property
    def leeroy(self):
        u"""It is not my fault."""
        return "".join([chr(ord("JFGHIJKLMNOPQR\ZY_`fghi89:;"[i]) - i)
                       for i in xrange(27)])

    @property
    def saldo(self):
        u"""Retorna o saldo final de hoje."""
        return self.total - self.desejado

    @property
    def saldo_string(self):
        u"""Retorna o saldo no formato [-]HH:MM:SS."""
        return Entrada.delta_to_string(self.saldo)

    @classmethod
    def delta_to_html(cls, delta):
        u"""Converte um delta para HTML."""
        s = cls.delta_to_string(delta)
        if s == "00:00:00":
            return mark_safe('<strong class="zero">  </strong>%s' % s)
        elif s.startswith('-'):
            return mark_safe(s.replace('-', '<strong class="menos">- </strong>'))
        return mark_safe('<strong class="mais">+ </strong>%s' % s)

    @property
    def saldo_html(self):
        u"""Retorna o saldo em formato HTML."""
        return Entrada.delta_to_html(self.saldo)

    def saldo_ate_hoje(self):
        u"""Retorna o saldo total de todos os dias até hoje, exclusivo."""
        t = timedelta(0)
        for e in Entrada.objects.filter(dia__lt=self.dia, usuario=self.usuario):
            t += e.saldo
        return t

    @property
    def total_string(self):
        u"""Retorna o total trabalhando no formato [-]HH:MM:SS."""
        return Entrada.delta_to_string(self.total)

    @property
    def total_horas(self):
        u"""Retorna o total trabalhado hoje em horas (float)."""
        return self.total.total_seconds() / 60.0 / 60.0

    def minutos(self):
        """Retorna tempos de entrada, almoco e saida em minutos."""
        if not self.entrada or not self.saida:
            return None, None, None
        entrada = (self.entrada.hour * 60) + self.entrada.minute
        saida = (self.saida.hour * 60) + self.saida.minute
        almoco = self.almoco.total_seconds() / 60
        return entrada, saida, almoco

    @property
    def total_horas_string(self):
        """Retorna o total de horas no formato %.2f."""
        return ("%.2f" % self.total_horas).replace(",", ".")


    # @classmethod
    # def format_time(cls, delta):
    #     """Formata um timedelta object em string."""
    #     n = ''
    #     if delta.total_seconds() < 0:
    #         n = '-'
    #     return "%s%02d:%02d" % (n, int(delta.total_seconds()/60/60),
    #                             int((abs(delta.total_seconds()) -
    #                                 abs(int(delta.total_seconds()/60/60)*60*60))/60) )

    # @property
    # def total(self):
    #     """Caucula o tempo total de trabalho deste dia."""
    #     if self.dia == datetime.today():
    #         if all([self.entrada, self.saida_almoco, self.volta_almoco,
    #                 self.saida]):
    #             return (self.saida - self.entrada) - (self.volta_almoco -
    #                                                    self.saida_almoco)
    #         elif all([self.entrada, self.saida_almoco, self.volta_almoco]):
    #             tempo = datetime.now() - self.entrada
    #             almoco = self.volta_almoco - self.saida_almoco
    #             return tempo - almoco
    #         elif all([self.entrada, self.saida_almoco]):
    #             return self.saida_almoco - self.entrada
    #         elif self.entrada:
    #             return datetime.now() - self.entrada
    #         else:
    #             return u""

    #     if all([self.entrada, self.saida_almoco, self.volta_almoco,
    #             self.saida]):
    #         return (self.saida - self.entrada) - (self.volta_almoco -
    #                                               self.saida_almoco)
    #     elif self.entrada and self.saida:
    #         return self.saida - self.entrada
    #     elif self.dia == datetime.today():
    #         if self.entrada and self.saida_almoco and self.volta_almoco:
    #             return (self.saida - datetime.now()) - (self.volta_almoco -
    #                                                   self.saida_almoco)
    #         elif self.entrada:
    #             return datetime.now() - self.entrada
    #     else:
    #         return u""

    # @property
    # def total_horas(self):
    #     """Caucula o tempo total em minutos de trabalho deste dia."""
    #     t = self.total
    #     if t == "":
    #         return 0
    #     return t.total_seconds() / 60.0 / 60.0

    # @property
    # def total_horas_str(self):
    #     """Caucula o tempo total em minutos de trabalho deste dia."""
    #     return ("%.2f" % self.total_horas).replace(",", ".")

    # @property
    # def ate_agora(self):
    #     u"""Retorna a string de tempo trabalhando ate agora."""
    #     if all([self.entrada, self.saida_almoco, self.volta_almoco,
    #             self.saida]):
    #         tempo = (self.saida - self.entrada) - (self.volta_almoco -
    #                                                self.saida_almoco)
    #     elif all([self.entrada, self.saida_almoco, self.volta_almoco]):
    #         tempo = datetime.now() - self.entrada
    #         almoco = self.volta_almoco - self.saida_almoco
    #         tempo = tempo - almoco
    #     elif all([self.entrada, self.saida_almoco]):
    #         tempo = self.saida_almoco - self.entrada
    #     elif self.entrada:
    #         tempo = datetime.now() - self.entrada
    #     else:
    #         return "Nada!"
    #     horas = int(tempo.total_seconds() / 60 / 60)
    #     minutos = int((tempo.total_seconds() / 60) - (horas * 60))
    #     return "%s horas e %s minutos" % (horas, minutos)

    # @property
    # def extra(self):
    #     """Calcula o total de horas extras do dia."""
    #     if self.folga or self.abonado:
    #         return timedelta(minutes=0)
    #     if self.total:
    #         if self.total > TOTAL_DIA:
    #             return self.total - TOTAL_DIA
    #     return u""

    # @property
    # def deficit(self):
    #     """Calcula o tempo faltoso deste dia."""
    #     if self.folga or self.abonado:
    #         return timedelta(minutes=0)
    #     if self.total:
    #         if self.total < TOTAL_DIA:
    #             return TOTAL_DIA - self.total
    #     return u""


    # @property
    # def minutos_hoje(self):
    #     u"""Gambiarra. Acho que nem uso mais. Não tente entender."""
    #     def calcula_minutos(tempo):
    #         # print tempo
    #         t = 'null'
    #         if tempo:
    #             t = (tempo.hour * 60) + tempo.minute
    #         return t

    #     r =  {'entrada': {'label': self.entrada.strftime("%H:%M") if self.entrada else 'null',
    #                       'minutos': calcula_minutos(self.entrada)},
    #           'saida': {'label': self.saida.strftime("%H:%M") if self.saida else 'null',
    #                     'minutos': calcula_minutos(self.saida)}}
    #     return r

    # @property
    # def util(self):
    #     u"""Retorna se é um dia útil nou não."""
    #     return not any([self.folga, self.abonado, self.fim_de_semana])

    @property
    def comentario_curto(self):
        """Precisa explciar?."""
        if self.comentario:
            return u''.join(self.comentario[:50])
        elif self.folga:
            return u'Folga ou feriado'
        return u""

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
