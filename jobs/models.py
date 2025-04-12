from django.db import models

# Create your models here.
from django.db import models

class JobPost(models.Model):
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    job_description = models.TextField(blank=True)
    apply_link = models.URLField()
    date_posted = models.DateTimeField(auto_now_add=True) #when the scraper saved the job
    job_posted_at = models.DateTimeField(null=True, blank=True) #when the job was actually posted 


    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

