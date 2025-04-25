"""
One-time script to update all subscription logos based on their names.
This script connects directly to the database without using the Flask application.
"""
import os
import sys
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get database URL from environment variable
DATABASE_URL = os.environ.get("DATABASE_URL")

# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Define a minimal Subscription model
class Subscription(Base):
    __tablename__ = 'subscription'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    logo_url = Column(String(255))

# Dictionary mapping service names to their logo URLs
service_logos = {
    'netflix': 'https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg',
    'spotify': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/spotify/spotify-original.svg',
    'apple': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/apple/apple-original.svg',
    'apple tv': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/apple/apple-original.svg',
    'apple music': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/apple/apple-original.svg',
    'amazon': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/amazonwebservices/amazonwebservices-original.svg',
    'amazon prime': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/amazonwebservices/amazonwebservices-original.svg',
    'google': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/google/google-original.svg',
    'google one': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/google/google-original.svg',
    'youtube': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/google/google-original.svg',
    'youtube premium': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/google/google-original.svg',
    'github': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg',
    'replit': 'https://replit.com/public/icons/apple-icon-180.png',
    'slack': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/slack/slack-original.svg',
    'microsoft': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/microsoft/microsoft-original.svg',
    'office 365': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/microsoft/microsoft-original.svg',
    'xbox': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/microsoft/microsoft-original.svg',
    'dropbox': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/dropbox/dropbox-original.svg',
    'adobe': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/adobe/adobe-original.svg',
    'photoshop': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/photoshop/photoshop-plain.svg',
    'digitalocean': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/digitalocean/digitalocean-original.svg',
    'hulu': 'https://upload.wikimedia.org/wikipedia/commons/e/e4/Hulu_Logo.svg',
    'disney+': 'https://upload.wikimedia.org/wikipedia/commons/3/3e/Disney%2B_logo.svg',
    'twitch': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/twitch/twitch-original.svg',
}

# Default logo for unknown services
default_logo = 'https://cdn-icons-png.flaticon.com/512/5053/5053352.png'

def get_logo_url_for_service(service_name):
    """Get a logo URL for a specific service based on its name."""
    # Check if we have a specific logo for this service
    # Try case-insensitive match
    service_name_lower = service_name.lower()
    for known_service, logo in service_logos.items():
        if known_service in service_name_lower:
            return logo
    
    return default_logo

def update_subscription_logos():
    """Update all subscription logo URLs based on their names."""
    # Get all subscriptions
    subscriptions = session.query(Subscription).all()
    updated_count = 0
    
    for subscription in subscriptions:
        # Always update logos (for this one-time script)
        old_logo = subscription.logo_url
        subscription.logo_url = get_logo_url_for_service(subscription.name)
        if old_logo != subscription.logo_url:
            updated_count += 1
    
    session.commit()
    return updated_count

if __name__ == "__main__":
    try:
        print("Updating subscription logos...")
        count = update_subscription_logos()
        print(f"Updated {count} subscription logos.")
    except Exception as e:
        print(f"Error updating logos: {str(e)}")
    finally:
        session.close()