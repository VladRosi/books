# Generated by Django 4.2.7 on 2023-11-29 13:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0006_alter_book_readers"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userbookrelation",
            name="rate",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (1, "Bad"),
                    (2, "Ok"),
                    (3, "Good"),
                    (4, "Amazing"),
                    (5, "Incredible"),
                ],
                null=True,
            ),
        ),
    ]
