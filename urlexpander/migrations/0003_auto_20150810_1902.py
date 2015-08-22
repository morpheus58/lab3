# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urlexpander', '0002_auto_20150810_1844'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expandedurls',
            old_name='destinationUrl',
            new_name='destination_url',
        ),
        migrations.RenameField(
            model_name='expandedurls',
            old_name='httpStatusCode',
            new_name='http_status_code',
        ),
        migrations.RenameField(
            model_name='expandedurls',
            old_name='pageTitle',
            new_name='page_title',
        ),
        migrations.RenameField(
            model_name='expandedurls',
            old_name='shortUrl',
            new_name='short_url',
        ),
    ]
