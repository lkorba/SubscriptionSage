# API Documentation

## Authentication Endpoints

### Register User
Endpoint for creating new user accounts. Validates email format and password strength.

```python
@bp.route('/auth/register', methods=['POST'])
def register():
    """Handle user registration with validation"""
    # Get and parse JSON request data
    data = request.get_json()
    
    # Validate required fields are present
    required_fields = ['email', 'password', 'name']
    if not all(field in data for field in required_fields):
        return jsonify({
            'status': 'error',
            'message': 'Missing required fields',
            'errors': {
                'fields': f"Required fields: {', '.join(required_fields)}"
            }
        }), 400
    
    # Validate email format
    if not validate_email(data['email']):
        return jsonify({
            'status': 'error',
            'message': 'Invalid email format',
            'errors': {
                'email': 'Please provide a valid email address'
            }
        }), 400
    
    # Validate password strength
    if not validate_password(data['password']):
        return jsonify({
            'status': 'error',
            'message': 'Password too weak',
            'errors': {
                'password': 'Password must be at least 8 characters and contain uppercase, lowercase, and numbers'
            }
        }), 400
    
    # Create new user
    user = User(
        email=data['email'],
        name=data['name']
    )
    user.set_password(data['password'])  # Hash password securely
    
    # Save to database
    db.session.add(user)
    db.session.commit()
    
    # Return success response
    return jsonify({
        'status': 'success',
        'message': 'User registered successfully',
        'data': {
            'user_id': user.id,
            'email': user.email,
            'name': user.name
        }
    }), 201
```

### Login
Endpoint for user authentication. Returns JWT token for subsequent requests.

```python
@bp.route('/auth/login', methods=['POST'])
def login():
    """Handle user authentication and token generation"""
    # Get and parse JSON request data
    data = request.get_json()
    
    # Validate required fields
    if not all(k in data for k in ['email', 'password']):
        return jsonify({
            'status': 'error',
            'message': 'Missing credentials',
            'errors': {
                'fields': 'Email and password are required'
            }
        }), 400
    
    # Find user by email
    user = User.query.filter_by(email=data['email']).first()
    
    # Verify user exists and password is correct
    if not user or not user.check_password(data['password']):
        return jsonify({
            'status': 'error',
            'message': 'Authentication failed',
            'error': 'Invalid credentials'
        }), 401
    
    # Generate JWT token
    access_token = create_access_token(identity=user.id)
    
    # Return success response with token
    return jsonify({
        'status': 'success',
        'message': 'Login successful',
        'data': {
            'token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name
            }
        }
    })
```

## Subscription Endpoints

### List Subscriptions
Retrieves all subscriptions for the authenticated user.

```python
@bp.route('/subscriptions', methods=['GET'])
@jwt_required()  # Require valid JWT token
def get_subscriptions():
    """Retrieve all subscriptions for authenticated user"""
    # Get user ID from JWT token
    user_id = get_jwt_identity()
    
    # Query all user subscriptions
    subscriptions = Subscription.query.filter_by(user_id=user_id).all()
    
    # Calculate total cost
    total_cost = sum(float(sub.amount) for sub in subscriptions)
    
    # Format response
    return jsonify({
        'status': 'success',
        'data': {
            'subscriptions': [{
                'id': sub.id,
                'name': sub.name,
                'amount': float(sub.amount),
                'currency': sub.currency,
                'billing_cycle': sub.billing_cycle,
                'next_billing_date': sub.next_billing_date.isoformat(),
                'logo_url': sub.logo_url
            } for sub in subscriptions],
            'total': len(subscriptions),
            'total_cost': total_cost
        }
    })
```

### Create Subscription
Creates a new subscription for the authenticated user.

```python
@bp.route('/subscriptions', methods=['POST'])
@jwt_required()  # Require valid JWT token
def create_subscription():
    """Create new subscription with validation"""
    # Get user ID from JWT token
    user_id = get_jwt_identity()
    
    # Get and parse JSON request data
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'amount', 'currency', 'billing_cycle']
    if not all(field in data for field in required_fields):
        return jsonify({
            'status': 'error',
            'message': 'Missing required fields',
            'errors': {
                'fields': f"Required fields: {', '.join(required_fields)}"
            }
        }), 400
    
    # Validate amount is positive
    try:
        amount = float(data['amount'])
        if amount <= 0:
            raise ValueError('Amount must be positive')
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': 'Invalid amount',
            'errors': {
                'amount': str(e)
            }
        }), 400
    
    # Validate billing cycle
    valid_cycles = ['monthly', 'yearly', 'quarterly']
    if data['billing_cycle'] not in valid_cycles:
        return jsonify({
            'status': 'error',
            'message': 'Invalid billing cycle',
            'errors': {
                'billing_cycle': f"Must be one of: {', '.join(valid_cycles)}"
            }
        }), 400
    
    # Create new subscription
    subscription = Subscription(
        user_id=user_id,
        name=data['name'],
        amount=amount,
        currency=data['currency'],
        billing_cycle=data['billing_cycle'],
        next_billing_date=calculate_next_billing_date(
            datetime.now(),
            data['billing_cycle']
        )
    )
    
    # Handle logo upload if provided
    if 'logo' in request.files:
        logo = request.files['logo']
        if logo and allowed_file(logo.filename):
            filename = secure_filename(logo.filename)
            logo_path = os.path.join('static/uploads/logos', filename)
            logo.save(logo_path)
            subscription.logo_url = f"/static/uploads/logos/{filename}"
    
    # Save to database
    db.session.add(subscription)
    db.session.commit()
    
    # Return success response
    return jsonify({
        'status': 'success',
        'message': 'Subscription created successfully',
        'data': {
            'id': subscription.id,
            'name': subscription.name,
            'amount': float(subscription.amount),
            'currency': subscription.currency,
            'billing_cycle': subscription.billing_cycle,
            'next_billing_date': subscription.next_billing_date.isoformat(),
            'logo_url': subscription.logo_url
        }
    }), 201
```

### Update Subscription
Modifies an existing subscription.

```python
@bp.route('/subscriptions/<int:id>', methods=['PUT'])
@jwt_required()  # Require valid JWT token
def update_subscription(id):
    """Update existing subscription with validation"""
    # Get user ID from JWT token
    user_id = get_jwt_identity()
    
    # Find subscription
    subscription = Subscription.query.filter_by(
        id=id,
        user_id=user_id
    ).first_or_404()
    
    # Get and parse JSON request data
    data = request.get_json()
    
    # Update fields if provided
    if 'name' in data:
        subscription.name = data['name']
    
    if 'amount' in data:
        try:
            amount = float(data['amount'])
            if amount <= 0:
                raise ValueError('Amount must be positive')
            subscription.amount = amount
        except ValueError as e:
            return jsonify({
                'status': 'error',
                'message': 'Invalid amount',
                'errors': {
                    'amount': str(e)
                }
            }), 400
    
    if 'currency' in data:
        subscription.currency = data['currency']
    
    if 'billing_cycle' in data:
        valid_cycles = ['monthly', 'yearly', 'quarterly']
        if data['billing_cycle'] not in valid_cycles:
            return jsonify({
                'status': 'error',
                'message': 'Invalid billing cycle',
                'errors': {
                    'billing_cycle': f"Must be one of: {', '.join(valid_cycles)}"
                }
            }), 400
        subscription.billing_cycle = data['billing_cycle']
        subscription.next_billing_date = calculate_next_billing_date(
            datetime.now(),
            data['billing_cycle']
        )
    
    # Save changes
    db.session.commit()
    
    # Return success response
    return jsonify({
        'status': 'success',
        'message': 'Subscription updated successfully',
        'data': {
            'id': subscription.id,
            'name': subscription.name,
            'amount': float(subscription.amount),
            'currency': subscription.currency,
            'billing_cycle': subscription.billing_cycle,
            'next_billing_date': subscription.next_billing_date.isoformat(),
            'logo_url': subscription.logo_url
        }
    })
```

### Delete Subscription
Removes a subscription.

```python
@bp.route('/subscriptions/<int:id>', methods=['DELETE'])
@jwt_required()  # Require valid JWT token
def delete_subscription(id):
    """Delete existing subscription"""
    # Get user ID from JWT token
    user_id = get_jwt_identity()
    
    # Find subscription
    subscription = Subscription.query.filter_by(
        id=id,
        user_id=user_id
    ).first_or_404()
    
    # Delete subscription
    db.session.delete(subscription)
    db.session.commit()
    
    # Return success response
    return jsonify({
        'status': 'success',
        'message': 'Subscription deleted successfully'
    })
```

## Report Endpoints

### Get Summary Report
Retrieves a summary of subscription spending.

```python
@bp.route('/reports/summary', methods=['GET'])
@jwt_required()  # Require valid JWT token
def get_summary_report():
    """Generate summary report of subscription spending"""
    # Get user ID from JWT token
    user_id = get_jwt_identity()
    
    # Get query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    currency = request.args.get('currency', 'USD')
    
    # Parse dates
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except (ValueError, TypeError):
        return jsonify({
            'status': 'error',
            'message': 'Invalid date format',
            'errors': {
                'dates': 'Dates must be in YYYY-MM-DD format'
            }
        }), 400
    
    # Query subscriptions in date range
    subscriptions = Subscription.query.filter(
        Subscription.user_id == user_id,
        Subscription.next_billing_date.between(start_date, end_date)
    ).all()
    
    # Calculate totals
    total_spent = sum(float(sub.amount) for sub in subscriptions)
    by_category = {}
    for sub in subscriptions:
        category = sub.category or 'uncategorized'
        if category not in by_category:
            by_category[category] = 0
        by_category[category] += float(sub.amount)
    
    # Calculate monthly average
    months = (end_date - start_date).days / 30
    monthly_average = total_spent / months if months > 0 else 0
    
    # Return summary report
    return jsonify({
        'status': 'success',
        'data': {
            'total_spent': total_spent,
            'subscription_count': len(subscriptions),
            'by_category': by_category,
            'monthly_average': monthly_average
        }
    })
```

### Get Detailed Report
Retrieves detailed transaction history.

```python
@bp.route('/reports/detailed', methods=['GET'])
@jwt_required()  # Require valid JWT token
def get_detailed_report():
    """Generate detailed report of subscription transactions"""
    # Get user ID from JWT token
    user_id = get_jwt_identity()
    
    # Get query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    currency = request.args.get('currency', 'USD')
    format = request.args.get('format', 'json')
    
    # Parse dates
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except (ValueError, TypeError):
        return jsonify({
            'status': 'error',
            'message': 'Invalid date format',
            'errors': {
                'dates': 'Dates must be in YYYY-MM-DD format'
            }
        }), 400
    
    # Query transactions in date range
    transactions = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.date.between(start_date, end_date)
    ).order_by(Transaction.date.desc()).all()
    
    # Format transactions
    formatted_transactions = [{
        'date': trans.date.isoformat(),
        'subscription': trans.subscription.name,
        'amount': float(trans.amount),
        'currency': trans.currency,
        'category': trans.subscription.category
    } for trans in transactions]
    
    # Calculate summary
    total = sum(float(trans.amount) for trans in transactions)
    
    # Return detailed report
    return jsonify({
        'status': 'success',
        'data': {
            'transactions': formatted_transactions,
            'summary': {
                'total': total,
                'count': len(transactions)
            }
        }
    })
```

## Settings Endpoints

### Get User Settings
Retrieves user preferences and settings.

```python
@bp.route('/settings', methods=['GET'])
@jwt_required()  # Require valid JWT token
def get_settings():
    """Retrieve user settings and preferences"""
    # Get user ID from JWT token
    user_id = get_jwt_identity()
    
    # Get user settings
    settings = UserSettings.query.filter_by(user_id=user_id).first()
    
    # Return settings
    return jsonify({
        'status': 'success',
        'data': {
            'default_currency': settings.default_currency,
            'notification_preferences': settings.notification_preferences,
            'theme': settings.theme
        }
    })
```

### Update Settings
Modifies user preferences and settings.

```python
@bp.route('/settings', methods=['PUT'])
@jwt_required()  # Require valid JWT token
def update_settings():
    """Update user settings and preferences"""
    # Get user ID from JWT token
    user_id = get_jwt_identity()
    
    # Get user settings
    settings = UserSettings.query.filter_by(user_id=user_id).first()
    
    # Get and parse JSON request data
    data = request.get_json()
    
    # Update settings if provided
    if 'default_currency' in data:
        settings.default_currency = data['default_currency']
    
    if 'notification_preferences' in data:
        settings.notification_preferences = data['notification_preferences']
    
    if 'theme' in data:
        valid_themes = ['light', 'dark', 'system']
        if data['theme'] not in valid_themes:
            return jsonify({
                'status': 'error',
                'message': 'Invalid theme',
                'errors': {
                    'theme': f"Must be one of: {', '.join(valid_themes)}"
                }
            }), 400
        settings.theme = data['theme']
    
    # Save changes
    db.session.commit()
    
    # Return updated settings
    return jsonify({
        'status': 'success',
        'message': 'Settings updated successfully',
        'data': {
            'default_currency': settings.default_currency,
            'notification_preferences': settings.notification_preferences,
            'theme': settings.theme
        }
    })
```

## Error Responses

### Validation Error
Response when request data fails validation.

```python
def handle_validation_error(error):
    """Handle validation errors with detailed messages"""
    return jsonify({
        'status': 'error',
        'message': 'Validation failed',
        'errors': {
            field: messages for field, messages in error.messages.items()
        }
    }), 400
```

### Authentication Error
Response when authentication fails.

```python
def handle_auth_error(error):
    """Handle authentication errors"""
    return jsonify({
        'status': 'error',
        'message': 'Authentication failed',
        'error': str(error)
    }), 401
```

### Not Found Error
Response when requested resource doesn't exist.

```python
def handle_not_found_error(error):
    """Handle not found errors"""
    return jsonify({
        'status': 'error',
        'message': 'Resource not found',
        'error': str(error)
    }), 404
```

## Rate Limiting

The API implements rate limiting to prevent abuse. Limits are:
- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated users

```python
# Rate limiting configuration
RATELIMIT_DEFAULT = "100 per minute"  # Default limit
RATELIMIT_STORAGE_URL = "memory://"   # Storage backend
RATELIMIT_STRATEGY = "fixed-window"   # Limiting strategy

# Rate limit decorator
@limiter.limit("100/minute")
@bp.route('/api/endpoint', methods=['GET'])
def rate_limited_endpoint():
    """Example of rate-limited endpoint"""
    pass
```

Rate limit headers:
```
X-RateLimit-Limit: 100      # Maximum requests allowed
X-RateLimit-Remaining: 95   # Remaining requests in current window
X-RateLimit-Reset: 1616248800  # Timestamp when limit resets
```

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <token>  # JWT token from login endpoint
```

Token format:
```python
# JWT token structure
{
    "sub": "user_id",        # Subject (user ID)
    "exp": 1616248800,       # Expiration timestamp
    "iat": 1616245200        # Issued at timestamp
}

# Token generation
def create_access_token(user_id):
    """Generate JWT access token"""
    return create_access_token(
        identity=user_id,
        expires_delta=timedelta(days=1)  # Token expires in 1 day
    )
```

## Best Practices

1. **Error Handling**
   - Use appropriate HTTP status codes
   - Provide detailed error messages
   - Include error codes for programmatic handling
   - Implement proper error logging

2. **Response Format**
   - Consistent JSON structure
   - Include status and message
   - Wrap data in a data object
   - Use proper content types

3. **Security**
   - Use HTTPS
   - Implement rate limiting
   - Validate input data
   - Sanitize output data
   - Use secure headers

4. **Performance**
   - Implement caching
   - Use pagination
   - Optimize response size
   - Compress responses
   - Use efficient queries 