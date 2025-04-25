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
