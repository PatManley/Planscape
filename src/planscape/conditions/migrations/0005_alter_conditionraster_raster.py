# Generated by Django 4.1.10 on 2023-08-16 20:30

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conditions', '0004_get_condition_pixels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conditionraster',
            name='raster',
            field=django.contrib.gis.db.models.fields.RasterField(null=True, srid=3857),
        ),
    ]