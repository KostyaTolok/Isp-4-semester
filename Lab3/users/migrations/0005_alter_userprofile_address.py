# Generated by Django 3.2 on 2021-05-21 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210521_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.CharField(blank=True, max_length=40, verbose_name='Адрес'),
        ),
    ]
