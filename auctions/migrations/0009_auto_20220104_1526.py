# Generated by Django 3.2.8 on 2022-01-04 12:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_listing_max_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'Active'), (0, 'Closed')], default=1),
        ),
        migrations.AddField(
            model_name='listing',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
