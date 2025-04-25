import requests
import logging
from datetime import datetime, timedelta
from flask import render_template
from flask_mail import Message
from app import app, db, mail
from models import ExchangeRate

logger = logging.getLogger(__name__)

def fetch_exchange_rates():
    """
    Fetch the latest exchange rates from an external API and update the database.
    Supports USD, EUR, CZK, and PLN.
    """
    try:
        # Using Exchange Rate API (free tier)
        api_key = app.config.get('EXCHANGE_RATE_API_KEY', 'fallback_key')
        base_url = "https://open.er-api.com/v6/latest/"
        
        # Fetch rates for each base currency
        base_currencies = ['USD', 'EUR', 'CZK', 'PLN']
        
        for base in base_currencies:
            url = f"{base_url}{base}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                rates = data.get('rates', {})
                
                # Update rates for each target currency
                for target in base_currencies:
                    if target != base and target in rates:
                        # Check if rate exists
                        exchange_rate = ExchangeRate.query.filter_by(
                            base_currency=base,
                            target_currency=target
                        ).first()
                        
                        if exchange_rate:
                            exchange_rate.rate = rates[target]
                            exchange_rate.updated_at = datetime.utcnow()
                        else:
                            exchange_rate = ExchangeRate(
                                base_currency=base,
                                target_currency=target,
                                rate=rates[target]
                            )
                            db.session.add(exchange_rate)
                
                db.session.commit()
                logger.info(f"Exchange rates for {base} updated successfully")
            else:
                logger.error(f"Failed to fetch exchange rates for {base}: {response.status_code}")
                
    except Exception as e:
        logger.error(f"Error updating exchange rates: {str(e)}")
        
    # If no exchange rates were fetched, add default ones
    if ExchangeRate.query.count() == 0:
        add_default_exchange_rates()

def add_default_exchange_rates():
    """Add default exchange rates if API fetch fails."""
    default_rates = [
        # USD to others
        {'base': 'USD', 'target': 'EUR', 'rate': 0.92},
        {'base': 'USD', 'target': 'CZK', 'rate': 22.89},
        {'base': 'USD', 'target': 'PLN', 'rate': 3.95},
        
        # EUR to others
        {'base': 'EUR', 'target': 'USD', 'rate': 1.09},
        {'base': 'EUR', 'target': 'CZK', 'rate': 24.97},
        {'base': 'EUR', 'target': 'PLN', 'rate': 4.31},
        
        # CZK to others
        {'base': 'CZK', 'target': 'USD', 'rate': 0.044},
        {'base': 'CZK', 'target': 'EUR', 'rate': 0.040},
        {'base': 'CZK', 'target': 'PLN', 'rate': 0.17},
        
        # PLN to others
        {'base': 'PLN', 'target': 'USD', 'rate': 0.25},
        {'base': 'PLN', 'target': 'EUR', 'rate': 0.23},
        {'base': 'PLN', 'target': 'CZK', 'rate': 5.79}
    ]
    
    for rate_data in default_rates:
        exchange_rate = ExchangeRate(
            base_currency=rate_data['base'],
            target_currency=rate_data['target'],
            rate=rate_data['rate']
        )
        db.session.add(exchange_rate)
    
    db.session.commit()
    logger.info("Default exchange rates added")

def convert_currency(amount, from_currency, to_currency):
    """Convert amount from one currency to another using stored exchange rates."""
    if from_currency == to_currency:
        return amount
    
    # Get exchange rate
    exchange_rate = ExchangeRate.query.filter_by(
        base_currency=from_currency,
        target_currency=to_currency
    ).first()
    
    if exchange_rate:
        return amount * exchange_rate.rate
    
    # If direct conversion not found, try via USD
    usd_from_rate = ExchangeRate.query.filter_by(
        base_currency=from_currency,
        target_currency='USD'
    ).first()
    
    usd_to_rate = ExchangeRate.query.filter_by(
        base_currency='USD',
        target_currency=to_currency
    ).first()
    
    if usd_from_rate and usd_to_rate:
        # Convert to USD first, then to target currency
        usd_amount = amount * (1 / usd_from_rate.rate)
        return usd_amount * usd_to_rate.rate
    
    # If no conversion path found, return original amount
    logger.warning(f"Could not find exchange rate from {from_currency} to {to_currency}")
    return amount

def format_currency(amount, currency):
    """Format amount with currency symbol."""
    currency_symbols = {
        'USD': '$',
        'EUR': '€',
        'CZK': 'Kč',
        'PLN': 'zł'
    }
    
    symbol = currency_symbols.get(currency, currency)
    
    if currency in ['CZK', 'PLN']:
        return f"{amount:.2f} {symbol}"
    else:
        return f"{symbol}{amount:.2f}"

def check_upcoming_reminders():
    """
    Check for subscriptions with upcoming payments and send reminders.
    This function is called by the scheduler.
    """
    from models import Subscription, Reminder, User
    
    # Get all active reminders
    reminders = Reminder.query.filter_by(is_sent=False).all()
    
    for reminder in reminders:
        subscription = Subscription.query.get(reminder.subscription_id)
        user = User.query.get(reminder.user_id)
        
        if not subscription or not user or not subscription.is_active:
            continue
        
        if not subscription.next_payment_date:
            continue
        
        # Check if it's time to send the reminder
        days_until_payment = (subscription.next_payment_date - datetime.utcnow()).days
        
        if days_until_payment <= reminder.days_before:
            # Send email reminder
            if reminder.email_notification and user.email:
                send_reminder_email(user, subscription, days_until_payment)
            
            # Mark reminder as sent
            reminder.is_sent = True
            db.session.commit()
            
            logger.info(f"Reminder sent for subscription {subscription.name} to user {user.username}")

def send_reminder_email(user, subscription, days_until_payment):
    """Send a reminder email for an upcoming subscription payment."""
    try:
        subject = f"Reminder: {subscription.name} payment due in {days_until_payment} days"
        
        msg = Message(
            subject=subject,
            recipients=[user.email]
        )
        
        msg.html = render_template(
            'email/payment_reminder.html',
            user=user,
            subscription=subscription,
            days_until_payment=days_until_payment,
            amount=format_currency(subscription.amount, subscription.currency)
        )
        
        mail.send(msg)
        logger.info(f"Reminder email sent to {user.email} for {subscription.name}")
    except Exception as e:
        logger.error(f"Failed to send reminder email: {str(e)}")

def reset_reminders_for_next_period():
    """Reset reminders for subscriptions that have been renewed."""
    from models import Subscription, Reminder
    
    # Get all subscriptions
    subscriptions = Subscription.query.filter_by(is_active=True).all()
    
    for subscription in subscriptions:
        # Calculate next payment date
        next_payment_date = subscription.calculate_next_payment_date()
        
        if next_payment_date:
            # Reset reminders for this subscription
            reminders = Reminder.query.filter_by(subscription_id=subscription.id).all()
            
            for reminder in reminders:
                reminder.is_sent = False
            
            db.session.commit()

def get_logo_url_for_service(service_name, url=None):
    """
    Get a logo URL for a specific service based on its name.
    If no match is found and URL is provided, attempt to get favicon from the website.
    """
    # Dictionary mapping service names to their logo URLs
    # Using popular service logos from CDNs for recognizable services
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
        'youtube': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/youtube/youtube-original.svg',
        'youtube premium': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/youtube/youtube-original.svg',
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
        'bolt': 'https://bolt.eu/favicon.ico',
        'cursor': 'https://cursor.sh/apple-icon-180.png',
        'gitlab': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/gitlab/gitlab-original.svg',
        'granola': 'https://granola.app/favicon.ico',
        'linear': 'https://asset.brandfetch.io/ideyqT5U_G/idWOGMQx-C.png',
        'lovable': 'https://lovable.ai/favicon.ico',
        'notability': 'https://notability.com/favicon.ico',
        'notion': 'https://www.notion.so/images/favicon.ico',
        'perplexity': 'https://www.perplexity.ai/favicon.ico',
        'perplexity ai': 'https://www.perplexity.ai/favicon.ico',
        'superhuman': 'https://superhuman.com/favicon.ico',
        'todoist': 'https://todoist.com/favicon.ico',
        'v0': 'https://v0.dev/favicon.ico',
    }
    
    # Default logo for unknown services
    default_logo = 'https://cdn-icons-png.flaticon.com/512/5053/5053352.png'
    
    # Check if we have a specific logo for this service
    # Try case-insensitive match
    service_name_lower = service_name.lower()
    for known_service, logo in service_logos.items():
        if known_service in service_name_lower:
            return logo
    
    # If URL is provided, try to get favicon from website
    if url:
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
            logging.error(f"Error fetching favicon for {url}: {str(e)}")
    
    return default_logo

def update_subscription_logos():
    """Update all subscription logo URLs based on their names."""
    from models import Subscription
    
    # Get all subscriptions
    subscriptions = Subscription.query.all()
    
    for subscription in subscriptions:
        if not subscription.logo_url:  # Only update if no logo URL exists
            subscription.logo_url = get_logo_url_for_service(subscription.name)
    
    db.session.commit()

def handle_image_upload(file, subscription_id):
    """
    Process image uploads for subscription logos
    - Validates file type
    - Resizes to max 200x200 px
    - Ensures file size is under 50KB
    - Saves to static/uploads directory with unique name
    
    Returns the URL path to the saved image or None if failed
    """
    import os
    from PIL import Image
    from io import BytesIO
    import uuid
    
    # Validate file extension
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
    if not file.filename or '.' not in file.filename:
        return None
        
    extension = file.filename.rsplit('.', 1)[1].lower()
    if extension not in allowed_extensions:
        return None
    
    # For SVG files, just save them directly (no resizing needed)
    if extension == 'svg':
        # Generate unique filename
        unique_filename = f"{subscription_id}_{uuid.uuid4().hex}.{extension}"
        upload_path = os.path.join('static', 'uploads', unique_filename)
        
        # Ensure file size is under 50KB (51200 bytes)
        file_content = file.read()
        if len(file_content) > 51200:
            return None
            
        # Save the file
        with open(upload_path, 'wb') as f:
            f.write(file_content)
            
        return f"/{upload_path}"  # Return relative URL path
    
    # For other image types, resize if needed
    try:
        # Read the image
        img = Image.open(BytesIO(file.read()))
        
        # Resize if larger than 200x200
        if img.width > 200 or img.height > 200:
            img.thumbnail((200, 200))
        
        # Save to memory to check size
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format=img.format or 'PNG')
        img_byte_arr.seek(0)
        
        # Check if file size is under 50KB
        if img_byte_arr.getbuffer().nbytes > 51200:  # 50KB in bytes
            # If too large, compress more aggressively
            quality = 85
            while img_byte_arr.getbuffer().nbytes > 51200 and quality > 20:
                img_byte_arr = BytesIO()
                img.save(img_byte_arr, format='JPEG', quality=quality, optimize=True)
                img_byte_arr.seek(0)
                quality -= 15
            
            # If still too large after compression
            if img_byte_arr.getbuffer().nbytes > 51200:
                return None
        
        # Generate unique filename
        unique_filename = f"{subscription_id}_{uuid.uuid4().hex}.{extension}"
        upload_path = os.path.join('static', 'uploads', unique_filename)
        
        # Save the file
        with open(upload_path, 'wb') as f:
            f.write(img_byte_arr.getvalue())
        
        return f"/{upload_path}"  # Return relative URL path
    
    except Exception as e:
        logging.error(f"Error processing uploaded image: {str(e)}")
        return None
