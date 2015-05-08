# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ponto', '0005_auto_20150226_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='folga',
            field=models.BooleanField(default=False, verbose_name='Folga ou feriado'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entrada',
            name='dia',
            field=models.DateField(default=datetime.datetime(2015, 2, 27, 16, 11, 24, 298805), unique=True, verbose_name='Dia'),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='entrada',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 27, 16, 11, 24, 298833), null=True, verbose_name='Entrada', blank=True),
        ),
    ]
