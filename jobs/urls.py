
from django.urls import path
from .views import job_list_view, JobPostListCreateView, run_scrapers_view



urlpatterns = [
    path("", job_list_view, name="home"),  # for homepage view
    # List all job posts or allow creating one manually GET
    path("jobs/", JobPostListCreateView.as_view(), name="job-list"),

    # Run all scrapers and save jobs to the DB via POST
    path("run-scrapers/", run_scrapers_view, name="run-scrapers"),



]
