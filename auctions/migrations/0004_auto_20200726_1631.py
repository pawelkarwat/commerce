# Generated by Django 3.0.8 on 2020-07-26 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20200726_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
    ]