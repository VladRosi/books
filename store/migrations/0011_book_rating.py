# Generated by Django 4.2.7 on 2023-12-02 14:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0010_remove_userbookrelation_discount_book_discount"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="rating",
            field=models.DecimalField(
                decimal_places=2, default=None, max_digits=3, null=True
            ),
        ),
    ]
