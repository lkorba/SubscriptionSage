# Development Guide for Subscription Tracker

This guide provides detailed instructions for setting up a development environment for the Subscription Tracker application.

## Required Dependencies

The application requires the following Python packages:

```
apscheduler>=3.10.0
email_validator>=2.0.0
Flask>=2.3.0
Flask-Login>=0.6.2
Flask-Mail>=0.9.1
Flask-SQLAlchemy>=3.0.0
gunicorn>=21.0.0
pandas>=2.0.0
Pillow>=10.0.0
psycopg2-binary>=2.9.6
requests>=2.28.0
trafilatura>=1.6.0
python-dotenv>=1.0.0
```

## Setting Up a Development Environment

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/subscription-tracker.git
cd subscription-tracker
```

### 2. Create and Activate a Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

Install all required packages:

```bash
# Install packages individually
pip install apscheduler email_validator Flask Flask-Login Flask-Mail Flask-SQLAlchemy gunicorn pandas Pillow psycopg2-binary requests trafilatura python-dotenv
```

### 4. Set Up PostgreSQL Database

1. Install PostgreSQL if not already installed
2. Create a new database for the application:

```bash
# Connect to PostgreSQL
psql -U postgres

# Create a database
CREATE DATABASE subscription_tracker;

# Create a user (optional)
CREATE USER tracker_user WITH PASSWORD 'your_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE subscription_tracker TO tracker_user;

# Exit PostgreSQL
\q
```

### 5. Set Up Environment Variables

Create a `.env` file in the root directory with the following variables:

```
# Database configuration
DATABASE_URL=postgresql://username:password@localhost:5432/subscription_tracker

# Flask configuration
FLASK_SECRET_KEY=your_very_secure_secret_key

# Mail server configuration (optional, for reminder emails)
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
MAIL_DEFAULT_SENDER=your_email@example.com
```

### 6. Initialize the Database

Run the application once to create all the necessary tables:

```bash
python main.py
```

### 7. Start the Development Server

```bash
# For development with auto-reloading
export FLASK_ENV=development  # On Windows: set FLASK_ENV=development
python main.py

# Or using gunicorn (for Linux/macOS)
gunicorn --bind 0.0.0.0:5000 --reload main:app
```

The application will be available at `http://localhost:5000`.

## Database Migrations

When making changes to database models:

1. Add or modify models in `models.py`
2. Create a migration script similar to `migrate_add_logo_url.py` for your changes
3. Run the migration script to update the database schema
4. Test thoroughly to ensure data integrity

Example migration script format:

```python
"""
Migration script to add new_column to table_name
"""
import os
import logging
from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connect to the database
DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define the model with the new column
class TableName(Base):
    __tablename__ = 'table_name'
    # Existing columns...
    new_column = Column(String(255))

# Perform the migration
try:
    # Add the new column
    engine.execute('ALTER TABLE table_name ADD COLUMN new_column VARCHAR(255)')
    logger.info("Migration successful: Added new_column to table_name")
except Exception as e:
    logger.error(f"Migration failed: {str(e)}")
    session.rollback()
finally:
    session.close()
```

## Code Style Guidelines

- Follow PEP 8 style guidelines for Python code
- Use 4 spaces for indentation (not tabs)
- Keep line length to a maximum of 100 characters
- Use meaningful variable and function names
- Add comments for complex logic
- Update docstrings when changing function behavior
- Write test cases for new features

## Testing

1. Create test files in a `tests/` directory
2. Use the `unittest` framework or `pytest` for testing
3. Create a separate test database for running tests

## Internationalization (i18n)

When adding new text to the application:

1. Add entries to the translation files in `static/locales/[language_code]/translation.json`
2. Use the translation functions in the templates and JavaScript code
3. Test the application in all supported languages

## Troubleshooting Common Issues

### Database Connection Issues

- Verify that PostgreSQL is running
- Check that the DATABASE_URL environment variable is correctly formatted
- Ensure the database user has the proper permissions

### Email Sending Issues

- Verify SMTP settings in the environment variables
- Check firewall settings if emails are not being sent
- Use a service like Mailtrap for testing email functionality

### Logo/Favicon Issues

- Troubleshoot with the browser developer tools to see if images are loading
- Check that the URLs in `utils.py` are accessible
- Verify that the Google Favicon service is responding correctly