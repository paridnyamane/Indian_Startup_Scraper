# Generated by Django 4.2.20 on 2025-04-12 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_jobpost_delete_jobposting'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpost',
            name='job_posted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
