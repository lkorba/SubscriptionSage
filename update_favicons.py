"""
One-time script to update all subscription logos with favicons from their URLs.
"""
import os
import logging
import sys
import requests
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up database connection
DB_URL = os.environ.get("DATABASE_URL")
if not DB_URL:
    raise ValueError("DATABASE_URL environment variable not set")

engine = create_engine(DB_URL)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Define model directly to avoid circular imports
class Base(DeclarativeBase):
    pass

class Subscription(Base):
    __tablename__ = 'subscription'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String(120), nullable=False)
    url = Column(String(255))
    logo_url = Column(String(255))
    amount = Column(Float, default=0.0)
    currency = Column(String(3), default="USD")
    billing_cycle = Column(String(20), nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    next_payment_date = Column(DateTime)
    notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Define the favicon function directly to avoid import issues
def get_favicon_from_url(service_name, url):
    """Try to get favicon directly from a URL."""
    if not url:
        return None
        
    try:
        # Parse the URL to get the domain
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        
        # Only continue if we have a valid domain
        if parsed_url.netloc:
            # Try common favicon locations
            favicon_urls = [
                f"{parsed_url.scheme}://{parsed_url.netloc}/favicon.ico",
                f"{parsed_url.scheme}://{parsed_url.netloc}/favicon.png",
                f"{parsed_url.scheme}://{parsed_url.netloc}/apple-touch-icon.png",
                f"{parsed_url.scheme}://{parsed_url.netloc}/apple-icon.png",
            ]
            
            # Use Google's favicon service as a fallback
            google_favicon = f"https://www.google.com/s2/favicons?domain={parsed_url.netloc}&sz=64"
            
            # Try direct favicon URLs first
            for favicon_url in favicon_urls:
                try:
                    response = requests.head(favicon_url, timeout=2)
                    if response.status_code == 200:
                        return favicon_url
                except:
                    pass
            
            # Fallback to Google's favicon service
            return google_favicon
    except Exception as e:
        logger.error(f"Error fetching favicon for {url}: {str(e)}")
    
    return None

def update_subscription_favicons():
    """Update all subscription logos to use favicons from URLs if available."""
    session = Session()
    
    try:
        # Get all subscriptions that have a URL set
        subscriptions = session.query(Subscription).filter(Subscription.url.isnot(None)).all()
        
        logger.info(f"Found {len(subscriptions)} subscriptions with URLs to check for favicon updates")
        
        # Counter for tracking updates
        update_count = 0
        
        for subscription in subscriptions:
            # Skip if no URL provided
            if not subscription.url:
                continue
                
            # Get favicon from URL
            favicon_url = get_favicon_from_url(subscription.name, subscription.url)
            
            # Update if favicon found and different from current logo
            if favicon_url and favicon_url != subscription.logo_url:
                old_logo = subscription.logo_url or 'None'
                subscription.logo_url = favicon_url
                update_count += 1
                logger.info(f"Updated logo for '{subscription.name}': {old_logo} -> {favicon_url}")
        
        # Commit changes
        session.commit()
        logger.info(f"Successfully updated {update_count} subscription logos with favicons")
    
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating subscription favicons: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    update_subscription_favicons()