# Generated by Django 5.0.2 on 2024-03-02 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lookups', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lookuphistory',
            name='last_update',
        ),
    ]
