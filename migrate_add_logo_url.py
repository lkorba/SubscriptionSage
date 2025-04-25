"""
Migration script to add logo_url column to subscription table
"""
from app import app, db
from sqlalchemy import text
from utils import get_logo_url_for_service

with app.app_context():
    # Get a connection from the database
    with db.engine.connect() as conn:
        # Add the column to the subscription table
        print("Adding logo_url column to subscription table...")
        conn.execute(text('ALTER TABLE subscription ADD COLUMN IF NOT EXISTS logo_url VARCHAR(255);'))
        conn.commit()
    
    # Update existing subscriptions with logo URLs
    print("Updating existing subscriptions with logo URLs...")
    from models import Subscription
    
    subscriptions = Subscription.query.all()
    count = 0
    
    for subscription in subscriptions:
        subscription.logo_url = get_logo_url_for_service(subscription.name)
        count += 1
    
    db.session.commit()
    print(f"Updated {count} subscriptions with logo URLs.")
    print("Migration completed successfully.")