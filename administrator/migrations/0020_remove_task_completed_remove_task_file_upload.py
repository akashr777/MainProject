# Generated by Django 5.1.5 on 2025-03-21 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0019_task_completed_task_file_upload'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='completed',
        ),
        migrations.RemoveField(
            model_name='task',
            name='file_upload',
        ),
    ]
