# Generated by Django 3.0 on 2020-01-01 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_task'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='patinet',
            new_name='patient',
        ),
    ]