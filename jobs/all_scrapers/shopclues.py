import requests
from bs4 import BeautifulSoup
from django.utils.timezone import now
import logging

# Set up a logger for this module
logger = logging.getLogger(__name__)

def clean_text(html):
    """
    Converts HTML to clean plain text by:
    - Removing tags
    - Normalizing whitespace and line breaks
    - Replacing non-breaking spaces

    Args:
        html (str): Raw HTML string

    Returns:
        str: Cleaned plain text
    """
    text = BeautifulSoup(html, "html.parser").get_text(separator="\n")
    text = text.replace('\xa0', ' ')
    return ' '.join(text.split())

def extract_job_title(h5):
    """Extracts and cleans the job title from a header tag."""
    title_text = h5.get_text(strip=True)
    if not title_text.lower().startswith("position:"):
        return None
    return title_text.replace("Position:", "").strip()

def extract_location(h5):
    """Attempts to extract job location from the next <b> tag."""
    location_tag = h5.find_next("b")
    if location_tag and "Location" in location_tag.get_text():
        return location_tag.get_text().replace("Location:", "").strip()
    return "Not specified"

def extract_description(h5):
    """Traverses siblings to compile the job description until next job header."""
    description_lines = []
    for sibling in h5.find_all_next():
        if sibling.name == "h5" and "position:" in sibling.get_text(strip=True).lower():
            break
        if sibling.name in ["p", "div", "ul", "ol"]:
            text = sibling.get_text(separator="\n", strip=True)
            if text:
                description_lines.append(text)
    return clean_text(" ".join(description_lines))

def shopclues_scraper():
    """
    Scrapes job listings from the ShopClues careers page.

    Returns:
        list[dict]: A list of job dictionaries with standardized fields.
    """
    url = "https://www.shopclues.com/current-opening.html"
    jobs = []

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"ShopClues request failed: {e}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    # Remove footer if it exists to avoid capturing it in the last job description
    footer = soup.find("footer") or soup.find("div", class_="footer")
    if footer:
        footer.extract()

    for h5 in soup.find_all("h5"):
        try:
            job_title = extract_job_title(h5)
            if not job_title:
                continue

            location = extract_location(h5)
            job_description = extract_description(h5)

            jobs.append({
                "job_title": job_title,
                "company_name": "ShopClues",
                "location": location,
                "job_description": job_description,
                "apply_link": "mailto:career@shopclues.com",
                "job_posted_at": now() 
            })
        except Exception as e:
            logger.warning(f"Error parsing a ShopClues job post: {e}")
            continue

    return jobs
