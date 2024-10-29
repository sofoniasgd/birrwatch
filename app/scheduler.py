""" APScheduler module to auto run scraping scripts at an interval"""

from apscheduler.schedulers.background import BackgroundScheduler
from .scraper.scraper import script_caller

scheduler = BackgroundScheduler(daemon=True)

def scheduled_scraping():
    """Function that will be scheduled to run scraping jobs."""
    script_caller()



# functions to Start and end the scheduler
def start_scheduler():
    # Schedule the job to run at 4 AM every day
    scheduler.add_job(scheduled_scraping, 'cron', hour=12, minute=15)
    """Starts the scheduler only if it's not already running."""
    if not scheduler.running:
        scheduler.start()
        print("started scheduler")

def stop_scheduler():
    scheduler.shutdown(wait=False)
    print("stopped scheduler")