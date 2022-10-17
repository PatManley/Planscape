# Generated by Django 4.1.1 on 2022-09-23 19:33

import django.contrib.gis.db.models.fields
from django.db import migrations, models
from typing import Tuple


class Migration(migrations.Migration):

    initial = True

    dependencies:list[Tuple[str, str]] = [
    ]

    operations = [
        migrations.CreateModel(
            name='Marker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
    ]
