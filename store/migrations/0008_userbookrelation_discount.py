# Generated by Django 4.2.7 on 2023-11-30 23:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0007_alter_userbookrelation_rate"),
    ]

    operations = [
        migrations.AddField(
            model_name="userbookrelation",
            name="discount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
        ),
    ]
