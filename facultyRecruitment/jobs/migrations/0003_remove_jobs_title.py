# Generated by Django 3.2 on 2021-06-07 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_auto_20210607_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobs',
            name='title',
        ),
    ]
