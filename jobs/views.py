from django.shortcuts import render
from django.utils.timezone import now
from datetime import timedelta
from rest_framework import generics
from .models import JobPost
from .serializer import JobPostSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from jobs.all_scrapers import run_all_scrapers
from django.core.paginator import Paginator

# New imports for the cleanup endpoint
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class JobPostListCreateView(generics.ListCreateAPIView):
    """
    GET: Returns a list of all job posts (most recent first).
    POST: Allows manual creation of a job post (typically not needed).
    """
    queryset = JobPost.objects.all().order_by('-date_posted')
    serializer_class = JobPostSerializer


@api_view(["POST"])
def run_scrapers_view(request):
    """
    API endpoint to manually trigger all scrapers,
    save new job postings to the database,
    and return a summary of what happened.

    This lets you refresh the job listings on demand.
    """
    #run all scrapers to collect job data
    scraped_jobs = run_all_scrapers()
    added_jobs = 0
    skipped_jobs = 0

    for job in scraped_jobs:
        # Basic deduplication implementation by checking for job title and company name to confirm uniquenesss
        exists = JobPost.objects.filter(
            job_title=job["job_title"],
            company_name=job["company_name"]
        ).exists()

        if not exists:
            #Saves the job to the database
            JobPost.objects.create(
                job_title=job["job_title"],
                company_name=job["company_name"],
                location=job["location"],
                job_description=job["job_description"],
                apply_link=job["apply_link"]
            )
            added_jobs += 1
        else:
            skipped_jobs += 1

    return Response({
        "message": "Scraping complete.",
        "total_scraped": len(scraped_jobs),
        "new_jobs_added": added_jobs,
        "duplicates_skipped": skipped_jobs,
    })

def job_list_view(request):
    filter = request.GET.get("posted", "")
    title_query = request.GET.get("title", "")
    location_query = request.GET.get("location", "")
    company_query = request.GET.get("company", "")

    jobs = JobPost.objects.all().order_by('-job_posted_at')
    # Apply post date filtering
    if filter == "24h":
        jobs = jobs.filter(job_posted_at__gte=now() - timedelta(days=1))
    elif filter == "3d":
        jobs = jobs.filter(job_posted_at__gte=now() - timedelta(days=3))
    elif filter == "7d":
        jobs = jobs.filter(job_posted_at__gte=now() - timedelta(days=7))
    elif filter == "30d":
        jobs = jobs.filter(job_posted_at__gte=now() - timedelta(days=30))

     # Title/location filter
    if title_query:
        jobs = jobs.filter(job_title__icontains=title_query)
    if location_query:
        jobs = jobs.filter(location__icontains=location_query)
    if company_query:
        jobs = jobs.filter(company_name__icontains=company_query)

    #  Pagination
    paginator = Paginator(jobs, 9)  # 9 jobs per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    

    return render(request, "jobs/home.html", {"jobs": page_obj, "filter": filter})
@csrf_exempt
@require_http_methods(["POST"])
def cleanup_remotive_jobs(request):
    rem_qs = JobPost.objects.filter(apply_link__icontains="remotive.com")
    # 2) Within those, find the “bad” ones missing allowed locations
    bad_qs = rem_qs.exclude(
        Q(location__icontains="india") |
        Q(location__icontains="remote") |
        Q(location__icontains="worldwide") |
        Q(location="")
    )
    # 3) Delete them
    deleted_count, _ = bad_qs.delete()
    return JsonResponse({"deleted": deleted_count})
