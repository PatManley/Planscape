# Generated by Django 4.1.10 on 2023-09-26 14:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("planning", "0004_scenarioresult_completed_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="scenarioresult",
            name="completed_at",
            field=models.DateTimeField(
                help_text="End of the Forsys run, in UTC timezone", null=True
            ),
        ),
        migrations.AlterField(
            model_name="scenarioresult",
            name="started_at",
            field=models.DateTimeField(
                help_text="Start of the Forsys run, in UTC timezone", null=True
            ),
        ),
    ]
