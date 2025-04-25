# Utility Scripts Documentation

This document describes the various utility scripts included with the Subscription Tracker application and how to use them.

## Logo and Favicon Management Scripts

The application includes several scripts for managing subscription logos and favicons:

### 1. update_logos.py

This script updates all subscription logos based on their names using predefined mappings.

**Purpose:**
- Sets default logos for subscriptions based on their names
- Uses a predefined mapping of service names to logo URLs
- Only updates subscriptions that don't already have a logo

**Usage:**
```bash
python update_logos.py
```

### 2. update_favicons.py

This script updates all subscription logos by attempting to fetch favicons directly from their websites.

**Purpose:**
- Fetches favicons from the website URLs of subscriptions
- More dynamic than predefined mappings, as it gets the actual site's icon
- Falls back to Google's favicon service if direct fetching fails

**Usage:**
```bash
python update_favicons.py
```

### 3. fix_logos.py

This script fixes any broken or missing subscription logos.

**Purpose:**
- Corrects broken logo references
- Updates all subscription logos, including those with existing logos
- Uses the same logic as update_logos.py but applies it to all subscriptions

**Usage:**
```bash
python fix_logos.py
```

## Database Management

### migrate_add_logo_url.py

This script adds the `logo_url` column to the subscription table.

**Purpose:**
- Used when migrating from a version without logo support
- Safely adds the new column without data loss
- Should only be run once when upgrading from an older version

**Usage:**
```bash
python migrate_add_logo_url.py
```

## Exchange Rate Management

The exchange rate functionality is built into the main application via scheduled tasks, but you can manually trigger an update:

### Manually Updating Exchange Rates

To manually update all exchange rates:

```python
# In a Python shell or script
from utils import fetch_exchange_rates
fetch_exchange_rates()
```

## Reminder Management

The application automatically manages reminders through scheduled tasks. To manually trigger reminder checks:

```python
# In a Python shell or script
from utils import check_upcoming_reminders, reset_reminders_for_next_period

# Check for reminders that need to be sent
check_upcoming_reminders()

# Reset reminders for subscriptions with renewed payment dates
reset_reminders_for_next_period()
```

## Creating New Utility Scripts

When creating new utility scripts, follow these guidelines:

1. **Standalone Functionality**: Scripts should be able to run independently
2. **Error Handling**: Include proper error handling and logging
3. **Database Connection**: Establish a direct database connection (don't rely on Flask)
4. **Documentation**: Add a descriptive docstring explaining the purpose
5. **Logging**: Use the logging module to provide meaningful feedback
6. **Idempotence**: When possible, make scripts safe to run multiple times

Example template for a new utility script:

```python
"""
Description of what this script does.
"""
import os
import logging
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection
DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define models
class SomeModel(Base):
    __tablename__ = 'some_table'
    id = Column(Integer, primary_key=True)
    # Define other columns as needed

def main_function():
    """Main functionality of the script."""
    try:
        # Your script logic here
        logger.info("Script completed successfully")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    main_function()
```