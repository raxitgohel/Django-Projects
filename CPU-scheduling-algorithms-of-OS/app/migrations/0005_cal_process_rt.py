# Generated by Django 4.0.3 on 2022-03-21 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_all_process'),
    ]

    operations = [
        migrations.AddField(
            model_name='cal_process',
            name='rt',
            field=models.IntegerField(null=True),
        ),
    ]