# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ponto', '0007_auto_20150227_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='usuario',
            field=models.ForeignKey(default=1, verbose_name='Funcionario', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='entrada',
            name='dia',
            field=models.DateField(default=datetime.datetime(2015, 3, 23, 0, 5, 8, 459282), unique=True, verbose_name='Dia'),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='entrada',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 23, 0, 5, 8, 459316), null=True, verbose_name='Entrada', blank=True),
        ),
    ]
