# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='data da cria\xe7\xe3o')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='data da atualiza\xe7\xe3o', auto_now_add=True)),
                ('dia', models.DateField(verbose_name='Dia')),
                ('entrada', models.DateTimeField(verbose_name='Entrada')),
                ('saida_almoco', models.DateTimeField(null=True, verbose_name='Sa\xedda para almo\xe7o', blank=True)),
                ('volta_almoco', models.DateTimeField(null=True, verbose_name='Volta do almo\xe7o', blank=True)),
                ('saida', models.DateTimeField(null=True, verbose_name='Sa\xedda', blank=True)),
                ('foto', models.ImageField(upload_to=b'fotos', null=True, verbose_name='Foto do ticket', blank=True)),
            ],
            options={
                'ordering': ('-dia',),
                'verbose_name': 'Entrada',
                'verbose_name_plural': 'Entrada',
            },
            bases=(models.Model,),
        ),
    ]
