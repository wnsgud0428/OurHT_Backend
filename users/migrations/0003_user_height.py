# Generated by Django 3.2.8 on 2021-11-11 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20211111_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='height',
            field=models.FloatField(null=True),
        ),
    ]
