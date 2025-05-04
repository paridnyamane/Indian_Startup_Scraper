# import requests
# from bs4 import BeautifulSoup
# from django.utils.timezone import now
# import logging
# import re

# # Set up a logger for this module
# logger = logging.getLogger(__name__)

# def clean_text(html):
#     """
#     Converts HTML to clean plain text by:
#     - Removing tags
#     - Normalizing whitespace and line breaks
#     - Replacing non-breaking spaces

#     Args:
#         html (str): Raw HTML string

#     Returns:
#         str: Cleaned plain text
#     """
#     text = BeautifulSoup(html, "html.parser").get_text(separator="\n")
#     text = re.sub(r"\n{2,}", "\n", text)  # Collapse multiple newlines
#     text = text.replace('\xa0', ' ')        # Replace non-breaking spaces
#     return text.strip()

# def remotive_scraper():
#     """
#     Scrapes remote jobs from the Remotive API.

#     Returns:
#         list[dict]: A list of job dictionaries with standardized fields.
#     """
#     url = "https://remotive.io/api/remote-jobs"
#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#     except requests.RequestException as e:
#         logger.error(f"Remotive request failed: {e}")
#         return []

#     jobs = []
#     try:
#         # Iterate over each job listing in the response
#         for job in response.json().get("jobs", []):
#             raw_html = job.get("description", "")
#             description = clean_text(raw_html)

#             jobs.append({
#                 "job_title": job.get("title", "No Title Provided"),
#                 "company_name": job.get("company_name", "Remotive"),
#                 "location": job.get("candidate_required_location", "Remote"),
#                 "job_description": description,
#                 "apply_link": job.get("url", ""),
#                 "job_posted_at": now()
#             })
#     except Exception as e:
#         logger.exception("Error parsing Remotive job data", exc_info=e)

#     return jobs
import logging
import re
import requests
from bs4 import BeautifulSoup
from django.utils.timezone import now

logger = logging.getLogger(__name__)


def clean_text(html: str) -> str:
    """
    Convert raw HTML to readable plain text.
    
    Strips tags, normalizes whitespace, and removes special characters.
    """
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n")
    text = re.sub(r"\n{2,}", "\n", text)           # Collapse multiple newlines
    return text.replace('\xa0', ' ').strip()       # Replace non-breaking spaces


def is_relevant_location(location: str) -> bool:
    """
    Check if a job location is relevant to Indian or global remote audiences.
    
    Keeps jobs where location is India, Remote, Worldwide, or unspecified.
    """
    if not location:
        return True  # Empty location is considered relevant
    
    location_lower = location.lower()
    return any(keyword in location_lower for keyword in ("india", "remote", "worldwide"))


def remotive_scraper() -> list[dict]:
    """
    Fetch and filter job listings from the Remotive API.

    Returns:
        A list of normalized job dictionaries.
    """
    api_url = "https://remotive.io/api/remote-jobs"

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.error("Remotive API request failed: %s", exc)
        return []

    try:
        raw_jobs = response.json().get("jobs", [])
    except Exception as exc:
        logger.exception("Failed to parse JSON response from Remotive", exc_info=exc)
        return []

    jobs = []
    for job in raw_jobs:
        location = job.get("candidate_required_location", "").strip()

        if not is_relevant_location(location):
            continue

        cleaned_description = clean_text(job.get("description", ""))

        jobs.append({
            "job_title": job.get("title", "No Title Provided"),
            "company_name": job.get("company_name", "Remotive"),
            "location": location or "Remote",
            "job_description": cleaned_description,
            "apply_link": job.get("url", ""),
            "job_posted_at": now()
        })

    logger.info("Remotive scraper collected %d relevant jobs", len(jobs))
    return jobs
