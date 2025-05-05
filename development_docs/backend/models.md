# Backend Models Documentation

## Database Models

### User Model
Core user model for authentication and profile management.

```python
class User(UserMixin, db.Model):
    """User model for authentication and profile management"""
    __tablename__ = 'users'  # Database table name
    
    # Primary key and essential fields
    id = db.Column(db.Integer, primary_key=True)  # Unique user identifier
    email = db.Column(db.String(120), unique=True, nullable=False)  # User's email address
    name = db.Column(db.String(100), nullable=False)  # User's display name
    password_hash = db.Column(db.String(128))  # Hashed password storage
    
    # Timestamps for record keeping
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Account creation time
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Last update time
    
    # Relationships to other models
    subscriptions = db.relationship('Subscription', backref='user', lazy='dynamic')  # User's subscriptions
    settings = db.relationship('UserSettings', backref='user', uselist=False)  # User's settings
    
    def set_password(self, password):
        """Securely hash and store password"""
        self.password_hash = generate_password_hash(password)  # Generate secure hash
    
    def check_password(self, password):
        """Verify password against stored hash"""
        return check_password_hash(self.password_hash, password)  # Compare password with hash
    
    def get_subscriptions(self):
        """Get all user subscriptions"""
        return self.subscriptions.all()  # Return all related subscriptions
```

### Subscription Model
Model for managing subscription services and payments.

```python
class Subscription(db.Model):
    """Subscription model for service subscriptions"""
    __tablename__ = 'subscriptions'  # Database table name
    
    # Primary key and foreign key
    id = db.Column(db.Integer, primary_key=True)  # Unique subscription identifier
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Owner user ID
    
    # Subscription details
    name = db.Column(db.String(100), nullable=False)  # Service name
    amount = db.Column(db.Numeric(10, 2), nullable=False)  # Subscription cost
    currency = db.Column(db.String(3), nullable=False)  # Currency code
    billing_cycle = db.Column(db.String(20), nullable=False)  # Billing frequency
    next_billing_date = db.Column(db.DateTime, nullable=False)  # Next payment date
    logo_url = db.Column(db.String(255))  # Service logo URL
    
    # Timestamps for record keeping
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Creation time
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Last update time
    
    # Relationships
    transactions = db.relationship('Transaction', backref='subscription', lazy='dynamic')  # Payment history
    
    def calculate_next_billing_date(self):
        """Calculate next billing date based on cycle"""
        if self.billing_cycle == 'monthly':
            return self.next_billing_date + timedelta(days=30)  # Add 30 days for monthly
        elif self.billing_cycle == 'yearly':
            return self.next_billing_date + timedelta(days=365)  # Add 365 days for yearly
        elif self.billing_cycle == 'quarterly':
            return self.next_billing_date + timedelta(days=90)  # Add 90 days for quarterly
        return self.next_billing_date  # Return current date if invalid cycle
    
    def get_transactions(self):
        """Get all transactions for this subscription"""
        return self.transactions.order_by(Transaction.date.desc()).all()  # Return sorted transactions
```

### UserSettings Model
Model for storing user preferences and settings.

```python
class UserSettings(db.Model):
    """User settings model for preferences"""
    __tablename__ = 'user_settings'  # Database table name
    
    # Primary key and foreign key
    id = db.Column(db.Integer, primary_key=True)  # Unique settings identifier
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Owner user ID
    
    # User preferences
    default_currency = db.Column(db.String(3), default='USD')  # Preferred currency
    notification_preferences = db.Column(db.JSON)  # Notification settings
    theme = db.Column(db.String(20), default='light')  # UI theme preference
    
    # Timestamps for record keeping
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Creation time
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Last update time
    
    def update_notification_preferences(self, preferences):
        """Update notification settings"""
        current = self.notification_preferences or {}  # Get current settings
        current.update(preferences)  # Update with new settings
        self.notification_preferences = current  # Save updated settings
```

### Transaction Model
Model for tracking subscription payments and renewals.

```python
class Transaction(db.Model):
    """Transaction model for payment tracking"""
    __tablename__ = 'transactions'  # Database table name
    
    # Primary key and foreign keys
    id = db.Column(db.Integer, primary_key=True)  # Unique transaction identifier
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Owner user ID
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.id'), nullable=False)  # Related subscription
    
    # Transaction details
    amount = db.Column(db.Numeric(10, 2), nullable=False)  # Payment amount
    currency = db.Column(db.String(3), nullable=False)  # Currency code
    date = db.Column(db.DateTime, nullable=False)  # Transaction date
    status = db.Column(db.String(20), nullable=False)  # Payment status
    
    # Timestamps for record keeping
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Creation time
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Last update time
    
    # Relationships
    user = db.relationship('User', backref='transactions')  # Related user
    
    def mark_as_paid(self):
        """Mark transaction as paid"""
        self.status = 'paid'  # Update status
        self.updated_at = datetime.utcnow()  # Update timestamp
```

## Model Methods

### User Authentication
Methods for user authentication and password management.

```python
def authenticate_user(email, password):
    """Authenticate user with email and password"""
    user = User.query.filter_by(email=email).first()  # Find user by email
    if user and user.check_password(password):  # Verify password
        return user  # Return user if authenticated
    return None  # Return None if authentication fails

def create_user(email, name, password):
    """Create new user with validation"""
    if User.query.filter_by(email=email).first():  # Check if email exists
        raise ValueError('Email already registered')  # Raise error if exists
    
    user = User(email=email, name=name)  # Create user instance
    user.set_password(password)  # Set password
    db.session.add(user)  # Add to session
    db.session.commit()  # Save to database
    return user  # Return created user
```

### Subscription Management
Methods for managing subscription data.

```python
def create_subscription(user_id, name, amount, currency, billing_cycle):
    """Create new subscription with validation"""
    # Validate amount
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError('Amount must be positive')
    except ValueError as e:
        raise ValueError(f'Invalid amount: {str(e)}')
    
    # Validate billing cycle
    valid_cycles = ['monthly', 'yearly', 'quarterly']
    if billing_cycle not in valid_cycles:
        raise ValueError(f'Invalid billing cycle. Must be one of: {", ".join(valid_cycles)}')
    
    # Create subscription
    subscription = Subscription(
        user_id=user_id,
        name=name,
        amount=amount,
        currency=currency,
        billing_cycle=billing_cycle,
        next_billing_date=calculate_next_billing_date(datetime.now(), billing_cycle)
    )
    
    db.session.add(subscription)  # Add to session
    db.session.commit()  # Save to database
    return subscription  # Return created subscription

def get_user_subscriptions(user_id):
    """Get all subscriptions for user"""
    return Subscription.query.filter_by(user_id=user_id).all()  # Return user's subscriptions

def update_subscription(subscription_id, user_id, **kwargs):
    """Update subscription with validation"""
    subscription = Subscription.query.filter_by(
        id=subscription_id,
        user_id=user_id
    ).first_or_404()  # Find subscription
    
    # Update fields
    for key, value in kwargs.items():
        if hasattr(subscription, key):  # Check if field exists
            setattr(subscription, key, value)  # Update field
    
    db.session.commit()  # Save changes
    return subscription  # Return updated subscription
```

## Data Validation

### Input Validation
Functions for validating user input data.

```python
def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'  # Email regex pattern
    return bool(re.match(pattern, email))  # Return True if email matches pattern

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:  # Check minimum length
        return False
    if not re.search(r'[A-Z]', password):  # Check for uppercase
        return False
    if not re.search(r'[a-z]', password):  # Check for lowercase
        return False
    if not re.search(r'\d', password):  # Check for number
        return False
    return True  # Password meets all requirements

def validate_currency(currency):
    """Validate currency code"""
    valid_currencies = ['USD', 'EUR', 'GBP', 'JPY']  # Supported currencies
    return currency.upper() in valid_currencies  # Check if currency is supported
```

### Data Sanitization
Functions for cleaning and sanitizing data.

```python
def sanitize_string(value):
    """Sanitize string input"""
    if not isinstance(value, str):  # Check if value is string
        return str(value)  # Convert to string
    return value.strip()  # Remove whitespace

def sanitize_amount(amount):
    """Sanitize monetary amount"""
    try:
        return float(amount)  # Convert to float
    except (ValueError, TypeError):
        raise ValueError('Invalid amount format')  # Raise error if invalid

def sanitize_date(date_str):
    """Sanitize date string"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')  # Parse date string
    except ValueError:
        raise ValueError('Invalid date format. Use YYYY-MM-DD')  # Raise error if invalid
```

## Database Migrations

### Migration Commands
Commands for managing database migrations.

```python
# Create new migration
flask db migrate -m "Add logo_url to subscriptions"  # Create migration file

# Apply migration
flask db upgrade  # Apply pending migrations

# Rollback migration
flask db downgrade  # Revert last migration
```

### Migration Example
Example migration file for adding logo URL support.

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

## Best Practices

1. **Model Design**
   - Use appropriate data types
   - Define relationships clearly
   - Include timestamps
   - Add indexes for performance

2. **Data Validation**
   - Validate input data
   - Sanitize user input
   - Handle edge cases
   - Provide clear error messages

3. **Security**
   - Hash sensitive data
   - Use parameterized queries
   - Implement access control
   - Validate permissions

4. **Performance**
   - Optimize queries
   - Use appropriate indexes
   - Implement caching
   - Monitor database usage

5. **Maintenance**
   - Document changes
   - Version control migrations
   - Regular backups
   - Monitor performance 