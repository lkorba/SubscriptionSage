# Backend Components Documentation

## Application Setup

### Main Application (app.py)
The main application file that initializes and configures the Flask application.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config  # Import configuration settings

# Initialize Flask extensions
db = SQLAlchemy()        # Database ORM
migrate = Migrate()      # Database migration tool
jwt = JWTManager()       # JWT authentication manager

def create_app(config_class=Config):
    """Application factory function that creates and configures the Flask app"""
    app = Flask(__name__)                    # Create Flask application instance
    app.config.from_object(config_class)     # Load configuration from class
    
    # Initialize extensions with app
    db.init_app(app)                         # Initialize database
    migrate.init_app(app, db)                # Initialize migrations
    jwt.init_app(app)                        # Initialize JWT
    
    # Register blueprints
    from app.auth import bp as auth_bp       # Import auth blueprint
    app.register_blueprint(auth_bp)          # Register auth routes
    
    from app.subscriptions import bp as subs_bp  # Import subscriptions blueprint
    app.register_blueprint(subs_bp)          # Register subscription routes
    
    # Register error handlers
    from app.errors import bp as errors_bp   # Import error handlers
    app.register_blueprint(errors_bp)        # Register error routes
    
    return app                              # Return configured application
```

Key Features:
- Application factory pattern for flexible configuration
- Environment-based settings management
- Modular blueprint structure
- Centralized error handling
- Secure JWT authentication

## Route Handlers

### Routes (routes.py)
Contains all API route handlers and business logic for the application.

```python
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Subscription
from app.utils import validate_email, validate_password

# Authentication Routes
@bp.route('/auth/register', methods=['POST'])
def register():
    """Handle user registration with validation"""
    data = request.get_json()                # Get JSON request data
    
    # Validate required fields
    if not all(k in data for k in ['email', 'password', 'name']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate email format
    if not validate_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Validate password strength
    if not validate_password(data['password']):
        return jsonify({'error': 'Password too weak'}), 400
    
    # Create new user
    user = User(
        email=data['email'],
        name=data['name']
    )
    user.set_password(data['password'])      # Hash password securely
    db.session.add(user)                     # Add to database session
    db.session.commit()                      # Commit changes
    
    return jsonify({
        'message': 'User registered successfully',
        'user_id': user.id
    }), 201

# Subscription Routes
@bp.route('/subscriptions', methods=['GET'])
@jwt_required()                             # Require JWT authentication
def get_subscriptions():
    """Retrieve all subscriptions for authenticated user"""
    user_id = get_jwt_identity()            # Get user ID from JWT
    user = User.query.get(user_id)          # Query user from database
    
    # Get all user subscriptions
    subscriptions = Subscription.query.filter_by(user_id=user_id).all()
    
    # Format response
    return jsonify({
        'subscriptions': [{
            'id': sub.id,
            'name': sub.name,
            'amount': float(sub.amount),
            'currency': sub.currency,
            'billing_cycle': sub.billing_cycle,
            'next_billing_date': sub.next_billing_date.isoformat()
        } for sub in subscriptions]
    })
```

Key Features:
- JWT-based authentication
- Input validation
- Error handling
- Response formatting
- Database operations

## Utility Functions

### Utils (utils.py)
Collection of utility functions used throughout the application.

```python
import re
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

def validate_email(email):
    """Validate email format using regex pattern"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))    # Return True if email matches pattern

def validate_password(password):
    """Validate password meets security requirements"""
    if len(password) < 8:                    # Check minimum length
        return False
    if not re.search(r'[A-Z]', password):    # Check for uppercase
        return False
    if not re.search(r'[a-z]', password):    # Check for lowercase
        return False
    if not re.search(r'\d', password):       # Check for number
        return False
    return True                              # Password meets all requirements

def calculate_next_billing_date(current_date, billing_cycle):
    """Calculate next billing date based on cycle"""
    if billing_cycle == 'monthly':
        return current_date + timedelta(days=30)  # Add 30 days for monthly
    elif billing_cycle == 'yearly':
        return current_date + timedelta(days=365) # Add 365 days for yearly
    elif billing_cycle == 'quarterly':
        return current_date + timedelta(days=90)  # Add 90 days for quarterly
    return current_date                          # Return current date if invalid cycle
```

Key Features:
- Email validation
- Password strength checking
- Date calculations
- Security functions

## Task Scheduler

### Scheduler (scheduler.py)
Background task scheduler for periodic operations.

```python
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.models import Subscription
from app.utils import send_notification

def init_scheduler():
    """Initialize and configure the task scheduler"""
    scheduler = BackgroundScheduler()        # Create scheduler instance
    
    # Schedule subscription renewal checks
    scheduler.add_job(
        check_subscription_renewals,         # Function to execute
        CronTrigger(hour=0, minute=0),       # Run at midnight
        id='renewal_check',                  # Unique job ID
        replace_existing=True                # Replace if exists
    )
    
    # Schedule payment reminders
    scheduler.add_job(
        send_payment_reminders,              # Function to execute
        CronTrigger(hour=9, minute=0),       # Run at 9 AM
        id='payment_reminders',              # Unique job ID
        replace_existing=True                # Replace if exists
    )
    
    scheduler.start()                        # Start the scheduler
    return scheduler

def check_subscription_renewals():
    """Check for upcoming subscription renewals"""
    # Get subscriptions due in next 7 days
    upcoming = Subscription.query.filter(
        Subscription.next_billing_date <= datetime.now() + timedelta(days=7)
    ).all()
    
    # Send notifications for each upcoming renewal
    for sub in upcoming:
        send_notification(
            user_id=sub.user_id,
            message=f"Your {sub.name} subscription renews in {sub.days_until_renewal} days"
        )
```

Key Features:
- Background task scheduling
- Cron-based triggers
- Error handling
- Notification system

## Asset Management Scripts

### Logo Update (update_logos.py)
Script for updating subscription service logos.

```python
import requests
from PIL import Image
from io import BytesIO
from app.models import Subscription
from app.utils import optimize_image

def update_subscription_logos():
    """Update logos for all subscription services"""
    # Get all subscriptions without logos
    subscriptions = Subscription.query.filter_by(logo_url=None).all()
    
    for sub in subscriptions:
        try:
            # Fetch logo from service API
            response = requests.get(f"https://api.logos.com/{sub.name}")
            if response.status_code == 200:
                # Process and optimize image
                img = Image.open(BytesIO(response.content))
                optimized = optimize_image(img)
                
                # Save to storage
                filename = f"{sub.name.lower()}.png"
                optimized.save(f"static/uploads/logos/{filename}")
                
                # Update subscription record
                sub.logo_url = f"/static/uploads/logos/{filename}"
                db.session.commit()
                
        except Exception as e:
            print(f"Error updating logo for {sub.name}: {str(e)}")
            continue
```

Key Features:
- Automated logo fetching
- Image optimization
- Error handling
- Database updates

### Favicon Update (update_favicons.py)
Script for updating website favicons.

```python
# Features:
- Favicon generation
- Multiple size support
- Format conversion
- Cache management
```

Key Features:
- Multi-size favicon generation
- Format optimization
- Cache management
- Error handling

### Logo Fix (fix_logos.py)
Script for fixing issues with existing logos.

```python
# Features:
- Logo validation
- Format correction
- Size adjustment
- Quality improvement
```

Key Features:
- Logo validation
- Format standardization
- Size optimization
- Quality enhancement

## Database Migration

### Logo URL Migration (migrate_add_logo_url.py)
Database migration script for adding logo URL support.

```python
"""Add logo_url column to subscriptions table

Revision ID: 1a2b3c4d5e6f
Revises: previous_revision
Create Date: 2024-03-20 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    """Add logo_url column to subscriptions table"""
    # Add new column with nullable constraint
    op.add_column('subscriptions',
        sa.Column('logo_url', sa.String(255), nullable=True)
    )
    
    # Create index for faster lookups
    op.create_index(
        'ix_subscriptions_logo_url',
        'subscriptions',
        ['logo_url']
    )

def downgrade():
    """Remove logo_url column from subscriptions table"""
    # Drop the index first
    op.drop_index('ix_subscriptions_logo_url')
    
    # Remove the column
    op.drop_column('subscriptions', 'logo_url')
```

Key Features:
- Schema modification
- Index creation
- Rollback support
- Data integrity

## Best Practices

1. **Code Organization**
   - Modular structure for maintainability
   - Clear separation of concerns
   - Consistent naming conventions
   - Comprehensive documentation

2. **Error Handling**
   - Try-except blocks for robustness
   - Detailed error messages
   - Proper logging
   - Graceful recovery

3. **Performance**
   - Database query optimization
   - Caching implementation
   - Background task processing
   - Resource management

4. **Security**
   - Input validation
   - Authentication checks
   - Data sanitization
   - Secure file handling

5. **Maintenance**
   - Version control
   - Testing coverage
   - Regular updates
   - Documentation updates 