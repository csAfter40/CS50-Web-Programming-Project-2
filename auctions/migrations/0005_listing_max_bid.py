# Generated by Django 3.2.8 on 2022-01-04 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='max_bid',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
    ]
