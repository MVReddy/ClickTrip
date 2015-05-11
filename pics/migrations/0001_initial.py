# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.FloatField(null=True)),
                ('city', models.FloatField(null=True)),
                ('country', django_countries.fields.CountryField(null=True, max_length=2)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('google_place_id', models.CharField(max_length=50, null=True)),
                ('foursquare_id', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pics',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('image', models.FilePathField()),
                ('source', models.CharField(max_length=100)),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
                ('location', models.ForeignKey(to='pics.Location', related_name='pictures')),
            ],
        ),
    ]
