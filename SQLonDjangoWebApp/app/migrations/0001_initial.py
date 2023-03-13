# Generated by Django 4.0.4 on 2022-04-27 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookID', models.TextField()),
                ('authorID', models.TextField()),
                ('bookName', models.TextField()),
                ('authorName', models.TextField()),
                ('status', models.BooleanField()),
            ],
        ),
    ]