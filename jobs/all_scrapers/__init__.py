# jobs/scrapers/__init__.py

from .remotive import remotive_scraper
from .shopclues import shopclues_scraper
from .paytm import paytm_scraper

def run_all_scrapers():
    """
    Runs all job scrapers and aggregates their results into a single list.

    Returns:
        list[dict]: Combined job postings from all sources.
    """
    all_jobs = []
    all_jobs.extend(remotive_scraper())
    all_jobs.extend(shopclues_scraper())
    all_jobs.extend(paytm_scraper())
    return all_jobs
