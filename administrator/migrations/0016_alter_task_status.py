# Generated by Django 5.1.5 on 2025-03-20 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0015_remove_employee_table_workload_remove_task_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('review', 'Review'), ('Completed', 'Completed')], default='Pending', max_length=20),
        ),
    ]
