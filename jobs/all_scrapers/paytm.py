import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime, timezone

# Set up a logger for this module
logger = logging.getLogger(__name__)

def paytm_scraper():
    """
    Scrapes job listings from Paytm's Lever job board.

    Returns:
        list[dict]: A list of job dictionaries with standardized fields.
    """
    url = "https://jobs.lever.co/paytm"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Paytm request failed: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    postings = soup.find_all("div", class_="posting")

    jobs = []
    for post in postings:
        try:
            # Extract core job info
            title = post.find("h5").get_text(strip=True)
            location = post.find("span", class_="location").get_text(strip=True)
            link_tag = post.find("a", class_="posting-btn-submit")
            apply_link = link_tag["href"] if link_tag else ""

            jobs.append({
                "job_title": title,
                "company_name": "Paytm",
                "location": location,
                "job_description": "",  # Optional: detail page fetch
                "apply_link": apply_link,
                "job_posted_at": datetime.now(timezone.utc) 

            })
        except Exception as e:
            logger.warning(f"Error parsing a Paytm job post: {e}")
            continue

    return jobs