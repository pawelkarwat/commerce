# Generated by Django 3.0.8 on 2020-08-02 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200726_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]
