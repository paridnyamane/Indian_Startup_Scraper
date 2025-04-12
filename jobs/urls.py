
from django.urls import path
from .views import JobPostListCreateView, run_scrapers_view, run_migrations_view

urlpatterns = [
    # List all job posts or allow creating one manually GET
    path("jobs/", JobPostListCreateView.as_view(), name="job-list"),

    # Run all scrapers and save jobs to the DB via POST
    path("run-scrapers/", run_scrapers_view, name="run-scrapers"),
    path('run-migrations/', run_migrations_view),

]