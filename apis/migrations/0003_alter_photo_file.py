# Generated by Django 3.2.8 on 2021-11-09 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0002_auto_20211022_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(upload_to='photos'),
        ),
    ]
