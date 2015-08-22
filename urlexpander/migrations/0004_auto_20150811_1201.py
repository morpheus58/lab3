# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urlexpander', '0003_auto_20150810_1902'),
    ]

    operations = [
        migrations.CreateModel(
            name='expandedurl',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('destination_url', models.URLField(default='')),
                ('short_url', models.URLField(default='http://')),
                ('http_status_code', models.IntegerField(default=0)),
                ('page_title', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='expandedurls',
        ),
    ]
