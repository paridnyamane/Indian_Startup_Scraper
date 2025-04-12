from django.urls import path
from .views import job_list_view

urlpatterns = [
    path("jobs/", job_list_view, name="job-list"),
]