# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ponto', '0006_auto_20150227_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='abonado',
            field=models.BooleanField(default=False, verbose_name='Falta abonada'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entrada',
            name='dia',
            field=models.DateField(default=datetime.datetime(2015, 2, 27, 16, 39, 58, 40537), unique=True, verbose_name='Dia'),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='entrada',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 27, 16, 39, 58, 40566), null=True, verbose_name='Entrada', blank=True),
        ),
    ]
