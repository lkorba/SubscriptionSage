# SubscriptionSage Development Guide

This guide will help you set up your development environment for working on SubscriptionSage using Dev Containers.

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop)
- [VS Code](https://code.visualstudio.com/) with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- Git

## Setup Instructions

### 1. Clone the Repository

```bash
git clone [repository-url]
cd SubscriptionSage
```

### 2. Open in VS Code with Dev Containers

1. Open the project in VS Code:
   ```bash
   code .
   ```

2. When prompted, click "Reopen in Container" or use the command palette (F1) and select "Dev Containers: Reopen in Container"

   This will:
   - Build the development container
   - Install all dependencies
   - Set up the PostgreSQL database
   - Configure the development environment

### 3. Environment Variables

The development container uses two types of environment variables:

1. Development settings (in `docker-compose.yml`):
```
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:postgres@db:5432/subscriptionsage
SESSION_SECRET=your-secret-key-here
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=subscriptionsage
```

2. User-specific settings (in `.env`):
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=noreply@subscriptiontracker.com
```

#### Getting an Exchange Rate API Key

The application uses the Exchange Rate API for currency conversion. To get an API key:

1. Visit [Exchange Rate API](https://www.exchangerate-api.com/)
2. Sign up for a free account
3. Navigate to your dashboard
4. Copy your API key
5. Add it to your `.env` file as `EXCHANGE_RATE_API_KEY`

The free tier includes:
- 1,500 requests per month
- Updates every 24 hours
- Support for USD, EUR, CZK, and PLN

If the API is unavailable, the application will use default exchange rates.

Important security notes:
- The `.env` file is automatically ignored by git (it's in `.gitignore`)
- Never commit sensitive credentials to version control
- Keep your `.env` file secure and don't share it
- For team development, use a secure method to share environment variables (like a password manager or secure vault)

### 4. Start the Development Server

The development server will start automatically when the container is built. You can access the application at http://localhost:5000.

If you need to restart the server:

```bash
docker compose down
docker compose up -d
```

## Development Workflow

1. Create a new branch for your feature or bugfix
2. Make your changes
3. Run the tests (if available)
4. Submit a pull request

## Project Structure

- `app.py`: Application setup and configuration
- `models.py`: Database models
- `routes.py`: URL route handlers
- `scheduler.py`: Background task scheduler
- `utils.py`: Utility functions
- `templates/`: HTML templates
- `static/`: Static files (CSS, JS, images)
- `.devcontainer/`: Dev container configuration
- `docker-compose.yml`: Docker services configuration
- `.env`: User-specific environment variables (not committed to git)

## Dev Container Features

The development container includes:

- Python 3.11
- PostgreSQL 16
- All required Python packages
- Pre-configured development environment
- Hot-reloading for development
- Integrated database management

## Notes

- The application uses Flask for web framework
- SQLAlchemy is used for database ORM
- Background tasks are handled by APScheduler
- All development is done inside a containerized environment
- No need to install Python or PostgreSQL locally
- Consistent development environment across all team members

# Development Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory with the following variables:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key_here
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_app_password_here
   ```
5. Initialize the database:
   ```bash
   flask db upgrade
   ```
6. Run the development server:
   ```bash
   flask run
   ```

## Exchange Rate API Setup

1. Sign up for a free API key at [exchangerate-api.com](https://www.exchangerate-api.com/)
2. Once you have your API key, go to the Reports page in the application
3. Click on "Manage API Key" and enter your API key
4. The exchange rates will be automatically updated

## Database Migrations

To create a new migration:
```bash
flask db migrate -m "Description of changes"
```

To apply migrations:
```bash
flask db upgrade
```

## Running Tests

```bash
python -m pytest
```

## Code Style

The project uses Black for code formatting. To format your code:
```bash
black .
```

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Run tests and ensure they pass
4. Submit a pull request
