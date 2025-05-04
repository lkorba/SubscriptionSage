# Utility Functions

This document describes the utility functions available in the SubscriptionSage application.

## Exchange Rates

The application uses the Exchange Rate API to fetch and update exchange rates. The rates are stored in the database and updated daily.

### Setup

1. Sign up for a free API key at [exchangerate-api.com](https://www.exchangerate-api.com/)
2. Go to the Reports page in the application
3. Click on "Manage API Key" and enter your API key
4. The exchange rates will be automatically updated

### Functions

- `fetch_exchange_rates()`: Fetches the latest exchange rates from the API and updates the database
- `convert_currency(amount, from_currency, to_currency)`: Converts an amount from one currency to another
- `format_currency(amount, currency)`: Formats an amount with the appropriate currency symbol

## Currency Management

### `fetch_exchange_rates()`

Fetches the latest exchange rates from an external API and updates the database.

- **Supported Currencies**: USD, EUR, CZK, PLN
- **API**: Uses [Exchange Rate API](https://www.exchangerate-api.com/) (free tier)
- **Fallback**: Adds default rates if API fetch fails
- **Usage**: Called by scheduler to keep rates updated

### `add_default_exchange_rates()`

Adds default exchange rates to the database if API fetch fails.

- **Default Rates**: Pre-configured rates for all supported currency pairs
- **Usage**: Internal function, called by `fetch_exchange_rates()`

### `convert_currency(amount, from_currency, to_currency)`

Converts an amount from one currency to another.

- **Parameters**:
  - `amount`: The amount to convert
  - `from_currency`: Source currency code
  - `to_currency`: Target currency code
- **Returns**: Converted amount
- **Fallback**: Returns original amount if conversion not possible

### `format_currency(amount, currency)`

Formats an amount with the appropriate currency symbol.

- **Parameters**:
  - `amount`: The amount to format
  - `currency`: Currency code
- **Returns**: Formatted string with currency symbol
- **Supported Currencies**: USD ($), EUR (€), CZK (Kč), PLN (zł)

## Reminder System

The application can send email reminders for upcoming subscription payments.

### Setup

1. Configure your email settings in the `.env` file:
   ```
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_app_password_here
   ```

### Functions

- `check_upcoming_reminders()`: Checks for upcoming payments and sends reminders
- `send_reminder_email(user, subscription, days_until_payment)`: Sends an email reminder
- `reset_reminders_for_next_period()`: Resets reminders for the next billing period

## Service Management

### `get_logo_url_for_service(service_name, url=None)`

Gets a logo URL for a specific service.

- **Parameters**:
  - `service_name`: Name of the service
  - `url`: Optional website URL for favicon fallback
- **Returns**: URL to service logo
- **Fallback**: Attempts to get favicon if no logo is found

### `update_subscription_logos()`

Updates logos for all subscriptions.

- **Usage**: Maintenance function
- **Actions**: Updates logos for all active subscriptions

### `handle_image_upload(file, subscription_id)`

Handles custom logo uploads for subscriptions.

- **Parameters**:
  - `file`: Uploaded file object
  - `subscription_id`: ID of the subscription
- **Returns**: Path to saved image
- **Security**: Validates file type and size

## Usage Examples

### Currency Conversion

```python
# Convert 100 USD to EUR
amount_eur = convert_currency(100, 'USD', 'EUR')

# Format the result
formatted_amount = format_currency(amount_eur, 'EUR')
```

### Reminder System

```python
# Check for upcoming reminders
check_upcoming_reminders()

# Reset reminders after renewal
reset_reminders_for_next_period()
```

### Service Logo Management

```python
# Get logo for a service
logo_url = get_logo_url_for_service('netflix')

# Update all subscription logos
update_subscription_logos()
```

## Dependencies

- Flask-Mail for email functionality
- Requests for API calls
- SQLAlchemy for database operations
- Logging for error tracking

## Error Handling

All utility functions include:
- Proper error logging
- Graceful fallbacks
- Exception handling
- Input validation

## Configuration

### Exchange Rate API Configuration

The application uses the Exchange Rate API for currency conversion. To set up the API:

1. **Get an API Key**:
   - Visit [Exchange Rate API](https://www.exchangerate-api.com/)
   - Sign up for a free account
   - Navigate to your dashboard
   - Copy your API key

2. **Configure the API Key**:
   - Add the key to your `.env` file:
     ```
     EXCHANGE_RATE_API_KEY=your_api_key_here
     ```
   - Or set it in `docker-compose.yml` for development:
     ```yaml
     environment:
       - EXCHANGE_RATE_API_KEY=your_api_key_here
     ```

3. **API Limits**:
   - Free tier: 1,500 requests per month
   - Rate updates: Every 24 hours
   - Supported currencies: USD, EUR, CZK, PLN

4. **Fallback Behavior**:
   - If API is unavailable, default rates are used
   - Default rates are updated manually when needed
   - Application continues to function with last known rates

### Email Configuration

See [Development Guide](DEVELOPMENT.md) for email configuration details. 