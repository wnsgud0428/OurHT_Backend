# Generated by Django 3.2.8 on 2021-11-11 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0005_rename_check_item_checklist_check_item_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='checklist',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='count_number',
        ),
        migrations.CreateModel(
            name='Motion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_number', models.IntegerField(null=True)),
                ('checklist', models.ManyToManyField(blank=True, related_name='exercises', to='exercises.Checklist')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercises.exercise')),
            ],
        ),
    ]
