# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ponto', '0011_auto_20150722_0013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entrada',
            name='abonado',
        ),
        migrations.RemoveField(
            model_name='entrada',
            name='folga',
        ),
        migrations.AlterField(
            model_name='entrada',
            name='dia',
            field=models.DateField(default=datetime.datetime(2015, 7, 22, 0, 28, 54, 790930), verbose_name='Dia'),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='tipo',
            field=models.CharField(default=b'util', max_length=20, verbose_name='Tipo', choices=[(b'util', 'Dia \xfatil'), (b'falta', 'Falta'), (b'folga', 'Folga ou feriado'), (b'abonado', 'Falta abonada'), (b'consumo', 'Consumo de hora extra')]),
        ),
    ]
