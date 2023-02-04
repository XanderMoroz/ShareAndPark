# Generated by Django 4.1.5 on 2023-02-04 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0004_alter_parkingplace_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkingplace',
            name='subway_station',
            field=models.CharField(choices=[('KSM', 'Комсомольская'), ('KRS', 'Курская')], default='KSM', max_length=3, verbose_name='Ближайшее метро'),
        ),
    ]