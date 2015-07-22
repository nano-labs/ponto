# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Entrada = apps.get_model("ponto", "Entrada")
    db_alias = schema_editor.connection.alias
    for e in Entrada.objects.all():
    	if e.folga:
    		e.tipo = 'folga'
    	elif e.abonado:
    		e.tipo = 'abonado'
    	e.save()

class Migration(migrations.Migration):

    dependencies = [
        ('ponto', '0010_auto_20150721_2354'),
    ]

    operations = [
	    migrations.RunPython(
	            forwards_func,
	        ),
    ]
