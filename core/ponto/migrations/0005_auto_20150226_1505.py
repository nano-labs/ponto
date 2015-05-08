# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ponto', '0004_auto_20150225_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrada',
            name='dia',
            field=models.DateField(default=datetime.datetime(2015, 2, 26, 15, 5, 44, 10156), unique=True, verbose_name='Dia'),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='entrada',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 26, 15, 5, 44, 10185), null=True, verbose_name='Entrada', blank=True),
        ),
    ]
