# Generated by Django 3.2.8 on 2022-01-04 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_max_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='max_bid',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=11),
        ),
    ]
