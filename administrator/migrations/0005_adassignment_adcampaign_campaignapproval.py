# Generated by Django 5.1.5 on 2025-03-15 05:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0004_adspace_timeslot'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_at', models.DateTimeField(auto_now_add=True)),
                ('ad_creative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.finaladcreative')),
                ('ad_space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.adspace')),
                ('time_slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.timeslot')),
            ],
        ),
        migrations.CreateModel(
            name='AdCampaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('budget', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Pending Approval', 'Pending Approval'), ('Approved', 'Approved'), ('Running', 'Running'), ('Completed', 'Completed')], default='Draft', max_length=20)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaigns', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CampaignApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_approved', models.BooleanField(default=False)),
                ('feedback', models.TextField(blank=True, null=True)),
                ('approved_at', models.DateTimeField(auto_now=True)),
                ('campaign', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='approval', to='administrator.adcampaign')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
