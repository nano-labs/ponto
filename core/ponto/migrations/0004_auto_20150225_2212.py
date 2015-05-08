# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ponto', '0003_auto_20150225_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrada',
            name='dia',
            field=models.DateField(default=datetime.datetime(2015, 2, 25, 22, 12, 52, 516706), unique=True, verbose_name='Dia'),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='entrada',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 25, 22, 12, 52, 516734), null=True, verbose_name='Entrada', blank=True),
        ),
    ]
