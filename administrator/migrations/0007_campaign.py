# Generated by Django 5.1.5 on 2025-03-15 05:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0006_remove_campaignapproval_campaign_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign_name', models.CharField(max_length=255)),
                ('budget', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('pending_budget', 'Pending Budget Approval'), ('approved', 'Approved'), ('running', 'Running'), ('completed', 'Completed'), ('rejected', 'Rejected')], default='pending_budget', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('campaign_request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='administrator.campaign_request')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaigns', to='administrator.user_table')),
            ],
        ),
    ]
