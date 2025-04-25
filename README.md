# Subscription Tracker

A comprehensive subscription management application designed to help users track, analyze, and optimize their recurring expenses. The application provides advanced financial insights with multi-currency support, robust localization features, and automated favicon updates for subscription tracking.

## Features

- **Multi-language Support**: English, Polish, and Czech languages
- **Multi-currency Handling**: USD, EUR, CZK, PLN with automatic exchange rate updates
- **Comprehensive Reporting**: Complete financial overview with CSV import/export
- **Reminder System**: Customizable email notifications for upcoming payments
- **Customizable Logos**: Upload custom subscription logos or use automatic favicon detection

## Screenshots

![Dashboard](attached_assets/image_1745622458004.png)
![Add Subscription](attached_assets/image_1745623405493.png)
![Subscription List](attached_assets/image_1745624321620.png)
![Reports](attached_assets/image_1745624767288.png)

## Quick Start

For a quick start guide on how to set up and run the application, see below. For more detailed development instructions, see [DEVELOPMENT.md](DEVELOPMENT.md) and [UTILITIES.md](UTILITIES.md).

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/subscription-tracker.git
cd subscription-tracker
```

### Step 2: Set Up a Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install flask flask-login flask-sqlalchemy flask-mail email-validator psycopg2-binary gunicorn pandas pillow apscheduler requests trafilatura python-dotenv
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory with the following variables:

```
# Database configuration
DATABASE_URL=postgresql://username:password@localhost:5432/subscription_tracker

# Flask configuration
FLASK_SECRET_KEY=your_very_secure_secret_key
```

### Step 5: Initialize the Database

1. Make sure your PostgreSQL server is running
2. Create a database called `subscription_tracker`
3. Run the Flask application once to create the tables:

```bash
python main.py
```

### Step 6: Start the Development Server

```bash
# For development
python main.py

# For production
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

The application will be available at `http://localhost:5000`.

## Additional Documentation

- [DEVELOPMENT.md](DEVELOPMENT.md) - Detailed guide for setting up a development environment
- [UTILITIES.md](UTILITIES.md) - Documentation for the utility scripts included with the application

## Project Structure

- `app.py` - Flask application and database initialization
- `main.py` - Application entry point
- `models.py` - Database models (User, Subscription, Reminder, ExchangeRate)
- `routes.py` - Application routes and view functions
- `utils.py` - Utility functions (currency conversion, logo handling, etc.)
- `scheduler.py` - Background task scheduling
- `static/` - Static files (CSS, JavaScript, images)
- `templates/` - Jinja2 HTML templates
- `migrate_add_logo_url.py` - Migration script for the logo_url feature
- `update_logos.py` - Script to update subscription logos
- `update_favicons.py` - Script to fetch favicons from websites
- `fix_logos.py` - Script to fix any broken logo references

## Adding New Features

### Adding a New Language

1. Create a new translation file in `static/locales/[language_code]/translation.json`
2. Add the language option to the registration and settings forms in the templates

### Adding a New Currency

1. Add the currency to the `fetch_exchange_rates` function in `utils.py`
2. Add the currency to the currency selection dropdown in the templates

### Creating a New Model

1. Define the model in `models.py`
2. Import the model in `app.py` to ensure it's created in the database
3. Create any necessary routes in `routes.py`
4. Create templates for displaying and editing the model

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.