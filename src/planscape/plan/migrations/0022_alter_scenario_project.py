# Generated by Django 4.1.3 on 2023-03-10 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("plan", "0021_alter_scenario_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="scenario",
            name="project",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="plan.project",
            ),
        ),
    ]
