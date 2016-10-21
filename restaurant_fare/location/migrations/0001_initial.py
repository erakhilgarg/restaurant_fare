# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entity_id', models.IntegerField()),
                ('entity_type', models.CharField(help_text=b'Entity Type', max_length=100)),
                ('address', models.CharField(default=b'', help_text=b'Address', max_length=100)),
                ('lat', models.FloatField(help_text=b'Lattitude')),
                ('lon', models.FloatField(help_text=b'Longitude')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-modified',),
            },
        ),
    ]
