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
