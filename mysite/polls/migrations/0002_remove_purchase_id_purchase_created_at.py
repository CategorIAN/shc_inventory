# Generated by Django 5.1 on 2024-08-23 18:11

import django.db.models.functions.datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='id',
        ),
        migrations.AddField(
            model_name='purchase',
            name='created_at',
            field=models.DateTimeField(db_default=django.db.models.functions.datetime.Now(), primary_key=True, serialize=False),
        ),
    ]
