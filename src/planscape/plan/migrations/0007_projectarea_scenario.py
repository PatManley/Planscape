# Generated by Django 4.1.3 on 2023-01-10 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0006_rename_generatedprojectareas_projectarea_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectarea',
            name='scenario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='plan.scenario'),
        ),
    ]