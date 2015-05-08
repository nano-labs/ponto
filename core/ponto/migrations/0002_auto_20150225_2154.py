# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ponto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='comentario',
            field=models.TextField(null=True, verbose_name='Coment\xe1rio', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entrada',
            name='dia',
            field=models.DateField(default=datetime.datetime(2015, 2, 25, 21, 54, 50, 622320), verbose_name='Dia'),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='entrada',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 25, 21, 54, 50, 622349), verbose_name='Entrada'),
        ),
    ]
