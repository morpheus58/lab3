# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urlexpander', '0004_auto_20150811_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='expandedurl',
            name='screen_capture',
            field=models.URLField(default='http://'),
        ),
    ]
