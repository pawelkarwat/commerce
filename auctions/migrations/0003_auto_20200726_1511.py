# Generated by Django 3.0.8 on 2020-07-26 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlisting_categories'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auctionlisting',
            old_name='categories',
            new_name='category',
        ),
    ]
