# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urlexpander', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='urlExpander',
            new_name='expandedurls',
        ),
        migrations.RenameField(
            model_name='expandedurls',
            old_name='DestinationUrl',
            new_name='destinationUrl',
        ),
    ]
