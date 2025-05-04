# SubscriptionSage

SubscriptionSage is a web application that helps users track and manage their subscriptions in one centralized location.

![SubscriptionSage Logo](https://example.com/logo.png)

## Overview

In today's digital economy, people often subscribe to numerous services across different platforms, making it difficult to keep track of all active subscriptions, billing cycles, and upcoming payments. SubscriptionSage solves this problem by providing a unified dashboard where users can manage all their subscription services.

## Features

- **Subscription Tracking**: Easily add, edit, and delete subscription services
- **Dashboard Overview**: Get a quick glance at your active subscriptions, monthly spending, and upcoming payments
- **Reminder System**: Set up email notifications for upcoming subscription renewals
- **Multi-Currency Support**: Track subscriptions in different currencies with automatic conversion to your preferred currency
- **Billing Cycle Management**: Support for weekly, monthly, quarterly, bi-annual, yearly, and lifetime subscriptions
- **Data Analysis**: Visualize your subscription spending patterns
- **Import/Export**: Import and export your subscription data as CSV files
- **User Profiles**: Personalized settings with language and currency preferences

## Technology Stack

- **Backend**: Flask (Python 3.11)
- **Database**: PostgreSQL 16 with SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Flask-Login
- **Email Notifications**: Flask-Mail
- **Background Tasks**: APScheduler
- **Development**: Docker & Dev Containers

## Quick Start

1. Clone the repository
2. Open in VS Code with Dev Containers extension
3. Create a `.env` file with your email settings (see [Development Guide](DEVELOPMENT.md))
4. The application will be available at http://localhost:5000

For detailed setup instructions, please see the [Development Guide](DEVELOPMENT.md).

## Usage

1. **Register/Login**: Create an account or sign in
2. **Add Subscriptions**: Enter details about your subscription services
3. **Set Reminders**: Configure when you want to be notified about upcoming payments
4. **Monitor Dashboard**: Track your spending and upcoming renewals
5. **Manage Subscriptions**: Update or cancel subscriptions as needed

## Screenshots

[Screenshots to be added here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For development setup instructions, see the [Development Guide](DEVELOPMENT.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For support or inquiries, please [contact me](mailto:lukasz.korbasiewicz@gmail.com).

---

SubscriptionSage - Take control of your digital subscriptions
