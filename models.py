from datetime import datetime, timedelta
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    language = db.Column(db.String(10), default="en")
    preferred_currency = db.Column(db.String(3), default="USD")
    
    # Relationships
    subscriptions = db.relationship('Subscription', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    reminders = db.relationship('Reminder', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(255))
    logo_url = db.Column(db.String(255))  # URL to the subscription's logo or icon
    amount = db.Column(db.Float, default=0.0)
    currency = db.Column(db.String(3), default="USD")
    billing_cycle = db.Column(db.String(20), nullable=False)  # weekly, monthly, quarterly, bi-annually, yearly, lifetime
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    next_payment_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    reminders = db.relationship('Reminder', backref='subscription', lazy='dynamic', cascade='all, delete-orphan')
    
    def calculate_next_payment_date(self):
        if self.billing_cycle == 'lifetime':
            return None
        
        if not self.next_payment_date or self.next_payment_date < datetime.utcnow():
            # Start from the start_date
            start = self.start_date
            
            # Calculate how many billing cycles have passed
            days_passed = (datetime.utcnow() - start).days
            
            if self.billing_cycle == 'weekly':
                weeks_passed = days_passed // 7
                self.next_payment_date = start + timedelta(days=(weeks_passed + 1) * 7)
            elif self.billing_cycle == 'monthly':
                # Simple approximation for months
                months_passed = days_passed // 30
                new_month = ((start.month - 1 + months_passed + 1) % 12) + 1
                new_year = start.year + ((start.month - 1 + months_passed + 1) // 12)
                self.next_payment_date = datetime(new_year, new_month, min(start.day, 28))
            elif self.billing_cycle == 'quarterly':
                quarters_passed = days_passed // 90
                new_month = ((start.month - 1 + (quarters_passed + 1) * 3) % 12) + 1
                new_year = start.year + ((start.month - 1 + (quarters_passed + 1) * 3) // 12)
                self.next_payment_date = datetime(new_year, new_month, min(start.day, 28))
            elif self.billing_cycle == 'bi-annually':
                half_years_passed = days_passed // 182
                new_month = ((start.month - 1 + (half_years_passed + 1) * 6) % 12) + 1
                new_year = start.year + ((start.month - 1 + (half_years_passed + 1) * 6) // 12)
                self.next_payment_date = datetime(new_year, new_month, min(start.day, 28))
            elif self.billing_cycle == 'yearly':
                years_passed = days_passed // 365
                self.next_payment_date = datetime(start.year + years_passed + 1, start.month, min(start.day, 28))
        
        return self.next_payment_date
    
    def __repr__(self):
        return f'<Subscription {self.name}>'

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'), nullable=False)
    days_before = db.Column(db.Integer, default=7)  # Days before payment to send reminder
    email_notification = db.Column(db.Boolean, default=True)
    push_notification = db.Column(db.Boolean, default=False)
    is_sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Reminder for Subscription {self.subscription_id} ({self.days_before} days before)>'

class ExchangeRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    base_currency = db.Column(db.String(3), nullable=False)
    target_currency = db.Column(db.String(3), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ExchangeRate {self.base_currency} to {self.target_currency}: {self.rate}>'
