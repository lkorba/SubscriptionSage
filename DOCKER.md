# Docker Development Environment

This project includes a complete Docker Compose setup for development with VS Code dev container support.

## Quick Start

1. Install the "Dev Containers" extension in VS Code
2. Open the project in VS Code
3. Press `F1` and select "Dev Containers: Reopen in Container"
4. Wait for the container to build and start

## Environment Variables

The following environment variables can be configured:

### Required
- `DATABASE_URL`: PostgreSQL connection string (default: `postgresql://postgres:postgres@db:5432/subscriptionsage`)
- `SESSION_SECRET`: Secret key for Flask sessions (default: `dev-secret-change-in-production`)

### Optional (Email Configuration)
- `MAIL_SERVER`: SMTP server (default: empty)
- `MAIL_PORT`: SMTP port (default: 587)
- `MAIL_USERNAME`: Email username (default: empty)
- `MAIL_PASSWORD`: Email password (default: empty)
- `MAIL_DEFAULT_SENDER`: Default sender email (default: `noreply@subscriptiontracker.com`)

## Services

- **web**: Flask application container
- **db**: PostgreSQL 16 database with health checks

## Development Features

- Automatic dependency installation
- Code formatting with Black
- Linting with Flake8
- Python testing with pytest
- Database management tools
- Hot reload for Flask development
- Persistent database storage

## Manual Setup

If you prefer not to use dev containers:

```bash
# Start services
docker-compose up -d

# Install dependencies in the container
docker-compose exec web pip install -r requirements.txt

# Run the Flask app
docker-compose exec web python app.py
```

## Security Notes

- Default credentials are for development only
- Change `SESSION_SECRET` for production deployments
- Mail configuration is optional and disabled by default 