# Backend Documentation

## Overview
The backend of SubscriptionSage is built using Python with Flask framework, SQLAlchemy for database operations, and various utility modules for specific functionalities. The application follows a modular architecture with clear separation of concerns.

## Directory Structure
```
backend/
├── app.py              # Main application entry point
├── routes.py           # Route definitions and handlers
├── models.py           # Database models
├── utils.py            # Utility functions
├── scheduler.py        # Background task scheduler
├── migrations/         # Database migrations
└── requirements.txt    # Python dependencies
```

## Key Components

### Core Files

1. **app.py**
   - Application initialization
   - Configuration setup
   - Database connection
   - Key features:
     - Flask app configuration
     - Database initialization
     - Blueprint registration
     - Error handlers

2. **routes.py**
   - API endpoint definitions
   - Request handling
   - Response formatting
   - Key endpoints:
     - User authentication
     - Subscription management
     - Report generation
     - Settings management

3. **models.py**
   - Database models
   - Relationships
   - Data validation
   - Key models:
     - User
     - Subscription
     - Payment
     - Settings

4. **utils.py**
   - Helper functions
   - Business logic
   - Data processing
   - Key utilities:
     - Date calculations
     - Currency conversion
     - File handling
     - Email sending

### Background Tasks

1. **scheduler.py**
   - Periodic task scheduling
   - Background job management
   - Key tasks:
     - Payment reminders
     - Report generation
     - Data cleanup

### Database

1. **Migrations**
   - Database schema changes
   - Version control
   - Data migrations

## API Endpoints

### Authentication
- POST /auth/register
- POST /auth/login
- POST /auth/logout
- GET /auth/profile

### Subscriptions
- GET /subscriptions
- POST /subscriptions
- GET /subscriptions/<id>
- PUT /subscriptions/<id>
- DELETE /subscriptions/<id>

### Reports
- GET /reports/summary
- GET /reports/detailed
- POST /reports/generate
- GET /reports/export

### Settings
- GET /settings
- PUT /settings
- POST /settings/logo
- DELETE /settings/logo

## Database Schema

### Users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Subscriptions
```sql
CREATE TABLE subscriptions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    name VARCHAR(255),
    amount DECIMAL,
    currency VARCHAR(3),
    billing_cycle VARCHAR(20),
    next_billing_date DATE,
    logo_url VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Security

1. **Authentication**
   - JWT token-based auth
   - Password hashing
   - Session management

2. **Authorization**
   - Role-based access
   - Resource ownership
   - Permission checks

3. **Data Protection**
   - Input validation
   - SQL injection prevention
   - XSS protection

## Error Handling

1. **HTTP Status Codes**
   - 200: Success
   - 400: Bad Request
   - 401: Unauthorized
   - 403: Forbidden
   - 404: Not Found
   - 500: Server Error

2. **Error Responses**
   - Consistent format
   - Detailed messages
   - Error codes

## Development Guidelines

1. **Code Style**
   - PEP 8 compliance
   - Docstring documentation
   - Type hints

2. **Testing**
   - Unit tests
   - Integration tests
   - API tests

3. **Performance**
   - Query optimization
   - Caching strategy
   - Resource management

4. **Deployment**
   - Docker containerization
   - Environment configuration
   - Database migrations 