# Generated by Django 3.2.8 on 2021-11-10 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0003_alter_photo_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='feedback',
        ),
        migrations.DeleteModel(
            name='Feedback',
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
