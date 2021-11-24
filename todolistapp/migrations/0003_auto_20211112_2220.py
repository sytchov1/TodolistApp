# Generated by Django 3.2.7 on 2021-11-12 19:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('todolistapp', '0002_todolist_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='completion_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='todolist',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
