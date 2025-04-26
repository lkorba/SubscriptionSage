# SubscriptionSage Development Guide

This guide will help you set up your development environment for working on SubscriptionSage.

## Prerequisites

- Python 3.11 or higher
- PostgreSQL database
- Git

## Setup Instructions

### 1. Clone the Repository

```bash
git clone [repository-url]
cd SubscriptionSage
```

### 2. Set Up Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file in the root directory with the following variables:

```
DATABASE_URL=postgresql://username:password@localhost:5432/subscription_sage
SESSION_SECRET=your_secret_key
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=noreply@subscriptiontracker.com
```

Replace the placeholder values with your actual configuration.

### 5. Set Up Database

Create a PostgreSQL database with the name specified in your DATABASE_URL.

### 6. Run Migrations

The application will automatically create tables when it starts.

### 7. Start the Development Server

```bash
python main.py
```

The application will be available at http://localhost:5000.

## Development Workflow

1. Create a new branch for your feature or bugfix
2. Make your changes
3. Run the tests (if available)
4. Submit a pull request

## Environmental Variables

- `DATABASE_URL`: Connection string for PostgreSQL database
- `SESSION_SECRET`: Secret key for session management
- `MAIL_SERVER`: SMTP server for sending emails
- `MAIL_PORT`: SMTP port
- `MAIL_USERNAME`: Email account username
- `MAIL_PASSWORD`: Email account password
- `MAIL_DEFAULT_SENDER`: Default email sender address

## Project Structure

- `app.py`: Application setup and configuration
- `models.py`: Database models
- `routes.py`: URL route handlers
- `scheduler.py`: Background task scheduler
- `utils.py`: Utility functions
- `templates/`: HTML templates
- `static/`: Static files (CSS, JS, images)

## Notes

- The application uses Flask for web framework
- SQLAlchemy is used for database ORM
- Background tasks are handled by APScheduler
