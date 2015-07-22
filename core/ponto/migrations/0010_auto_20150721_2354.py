# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ponto', '0009_auto_20150603_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='tipo',
            field=models.CharField(default=b'util', max_length=20, verbose_name='Tipo', choices=[(b'util', 'Dia \xfatil'), (b'falta', 'Falta'), (b'folga', 'Folga ou feriado'), (b'abodado', 'Falta abonada'), (b'consumo', 'Consumo de hora extra')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entrada',
            name='dia',
            field=models.DateField(default=datetime.datetime(2015, 7, 21, 23, 54, 36, 33237), verbose_name='Dia'),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='entrada',
            field=models.DateTimeField(null=True, verbose_name='Entrada', blank=True),
        ),
    ]
