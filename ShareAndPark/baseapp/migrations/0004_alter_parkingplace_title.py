# Generated by Django 4.1.5 on 2023-02-04 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0003_alter_сheque_options_order_creation_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingplace',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Адрес'),
        ),
    ]