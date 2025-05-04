
from django.db import migrations, models
from django.db.models import Q

def cleanup_remotive(apps, schema_editor):
    JobPost = apps.get_model('jobs', 'JobPost')
    # delete Remotive-sourced jobs whose location isn’t India, Remote, or Worldwide
    JobPost.objects.filter(company_name='Remotive') \
        .exclude(
            Q(location__icontains='india') |
            Q(location__icontains='remote') |
            Q(location__icontains='worldwide') |
            Q(location='')  # keep blank if you like
        ).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('jobs', '0003_jobpost_job_posted_at'),  
    ]

    operations = [
        migrations.RunPython(cleanup_remotive),
    ]
