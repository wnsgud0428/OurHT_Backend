# Generated by Django 3.2.8 on 2021-12-02 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0010_alter_exercise_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='motion',
            name='hip_x',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='motion',
            name='hip_y',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='motion',
            name='shoulder_x',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='motion',
            name='shoulder_y',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='created',
            field=models.DateTimeField(null=True),
        ),
    ]
