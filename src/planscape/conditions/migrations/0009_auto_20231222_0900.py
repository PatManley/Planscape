# Generated by Django 4.1.10 on 2023-11-28 13:46

from django.db import migrations


def handle(apps, schema_editor):
    BaseCondition = apps.get_model("conditions", "BaseCondition")
    bad_slope = BaseCondition.objects.filter(
        region_name="sierra-nevada",
        display_name="Wildland Urban Interface",
        condition_name="slope",
    )

    if bad_slope.count() > 1:
        print("This migration is BAD! Check manually")
        return

    instance = bad_slope.first()
    if instance:
        instance.condition_name = "wui"
        instance.save()


class Migration(migrations.Migration):
    dependencies = [
        ("conditions", "0008_auto_20231128_1346"),
    ]

    operations = [migrations.RunPython(handle)]
