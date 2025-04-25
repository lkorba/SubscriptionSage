from apscheduler.schedulers.background import BackgroundScheduler
from app import app
from utils import fetch_exchange_rates, check_upcoming_reminders, reset_reminders_for_next_period
import logging

logger = logging.getLogger(__name__)

def init_scheduler():
    """Initialize the scheduler for recurring tasks."""
    scheduler = BackgroundScheduler()
    
    # Update exchange rates daily
    scheduler.add_job(
        fetch_exchange_rates,
        'interval',
        days=1,
        id='update_exchange_rates',
        replace_existing=True
    )
    
    # Check for reminders hourly
    scheduler.add_job(
        check_upcoming_reminders,
        'interval',
        hours=1,
        id='check_reminders',
        replace_existing=True
    )
    
    # Reset reminders daily
    scheduler.add_job(
        reset_reminders_for_next_period,
        'interval',
        days=1,
        id='reset_reminders',
        replace_existing=True
    )
    
    # Start the scheduler
    scheduler.start()
    logger.info("Scheduler started")
    
    # Run immediately to initialize data
    fetch_exchange_rates()
    
    return scheduler
