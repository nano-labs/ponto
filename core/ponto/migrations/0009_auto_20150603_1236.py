# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ponto', '0008_auto_20150323_0005'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntradaTodos',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('ponto.entrada',),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='dia',
            field=models.DateField(default=datetime.datetime(2015, 6, 3, 12, 36, 22, 400563), verbose_name='Dia'),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='entrada',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 3, 12, 36, 22, 400587), null=True, verbose_name='Entrada', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='entrada',
            unique_together=set([('usuario', 'dia')]),
        ),
    ]
