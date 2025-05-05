# Frontend Templates Documentation

## Template Structure

### Base Template (base.html)
The base template serves as the foundation for all pages in the application. It defines the common structure and includes essential meta tags, CSS, and JavaScript files.

```html
<!DOCTYPE html>
<html lang="{{ g.locale }}">
<head>
    <!-- Meta tags for SEO and viewport settings -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{{ _('Subscription management application') }}">
    
    <!-- Page title with dynamic content -->
    <title>{% block title %}{{ _('SubscriptionSage') }}{% endblock %}</title>
    
    <!-- Favicon and theme color -->
    <link rel="icon" type="image/png" href="{{ url_for('static', filename='favicon.png') }}">
    <meta name="theme-color" content="#4A90E2">
    
    <!-- CSS stylesheets -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/forms.css') }}">
    {% block styles %}{% endblock %}
    
    <!-- JavaScript libraries -->
    <script src="{{ url_for('static', filename='js/main.js') }}" defer></script>
    {% block scripts %}{% endblock %}
</head>
<body class="theme-{{ g.theme }}">
    <!-- Navigation header -->
    <header class="main-header">
        <nav class="nav-container">
            <!-- Logo and brand -->
            <a href="{{ url_for('main.index') }}" class="brand">
                <img src="{{ url_for('static', filename='logo.png') }}" alt="SubscriptionSage">
            </a>
            
            <!-- Main navigation menu -->
            <ul class="nav-menu">
                {% if current_user.is_authenticated %}
                    <li><a href="{{ url_for('main.dashboard') }}">{{ _('Dashboard') }}</a></li>
                    <li><a href="{{ url_for('main.subscriptions') }}">{{ _('Subscriptions') }}</a></li>
                    <li><a href="{{ url_for('main.reports') }}">{{ _('Reports') }}</a></li>
                    <li><a href="{{ url_for('main.settings') }}">{{ _('Settings') }}</a></li>
                {% else %}
                    <li><a href="{{ url_for('auth.login') }}">{{ _('Login') }}</a></li>
                    <li><a href="{{ url_for('auth.register') }}">{{ _('Register') }}</a></li>
                {% endif %}
            </ul>
            
            <!-- User menu for authenticated users -->
            {% if current_user.is_authenticated %}
                <div class="user-menu">
                    <img src="{{ current_user.avatar_url }}" alt="{{ current_user.name }}" class="avatar">
                    <div class="dropdown">
                        <a href="{{ url_for('main.profile') }}">{{ current_user.name }}</a>
                        <a href="{{ url_for('auth.logout') }}">{{ _('Logout') }}</a>
                    </div>
                </div>
            {% endif %}
        </nav>
    </header>
    
    <!-- Flash messages for user feedback -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <div class="flash-messages">
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">
                        {{ message }}
                        <button type="button" class="close">&times;</button>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    {% endwith %}
    
    <!-- Main content area -->
    <main class="main-content">
        {% block content %}{% endblock %}
    </main>
    
    <!-- Footer with links and copyright -->
    <footer class="main-footer">
        <div class="footer-content">
            <div class="footer-links">
                <a href="{{ url_for('main.about') }}">{{ _('About') }}</a>
                <a href="{{ url_for('main.contact') }}">{{ _('Contact') }}</a>
                <a href="{{ url_for('main.privacy') }}">{{ _('Privacy') }}</a>
                <a href="{{ url_for('main.terms') }}">{{ _('Terms') }}</a>
            </div>
            <div class="copyright">
                &copy; {{ now.year }} SubscriptionSage. {{ _('All rights reserved.') }}
            </div>
        </div>
    </footer>
</body>
</html>
```

### Dashboard (dashboard.html)
The main dashboard view showing subscription overview and statistics. This template extends the base template and implements a responsive grid layout for displaying subscription information.

Key Features:
- Subscription summary cards
- Recent activity feed
- Quick action buttons
- Data visualization charts

Template Structure:
```html
{% extends "base.html" %}

{% block title %}{{ _('Dashboard') }} - {{ _('SubscriptionSage') }}{% endblock %}

{% block styles %}
<!-- Additional styles for dashboard -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/dashboard.css') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='css/charts.css') }}">
{% endblock %}

{% block content %}
<div class="dashboard-container">
    <!-- Summary cards -->
    <div class="summary-cards">
        <!-- Total spending card -->
        <div class="card">
            <h3>{{ _('Total Spending') }}</h3>
            <div class="amount">{{ total_spending|currency }}</div>
            <div class="trend {{ spending_trend }}">
                {{ spending_change }}% {{ _('from last month') }}
            </div>
        </div>
        
        <!-- Active subscriptions card -->
        <div class="card">
            <h3>{{ _('Active Subscriptions') }}</h3>
            <div class="count">{{ subscriptions|length }}</div>
            <div class="trend {{ subscriptions_trend }}">
                {{ subscriptions_change }}% {{ _('from last month') }}
            </div>
        </div>
        
        <!-- Upcoming payments card -->
        <div class="card">
            <h3>{{ _('Upcoming Payments') }}</h3>
            <div class="amount">{{ upcoming_payments|currency }}</div>
            <div class="date">{{ next_payment_date|date }}</div>
        </div>
    </div>
    
    <!-- Spending chart -->
    <div class="chart-container">
        <h2>{{ _('Spending Overview') }}</h2>
        <canvas id="spendingChart"></canvas>
    </div>
    
    <!-- Recent subscriptions -->
    <div class="recent-subscriptions">
        <h2>{{ _('Recent Subscriptions') }}</h2>
        <div class="subscription-list">
            {% for subscription in recent_subscriptions %}
                <div class="subscription-card">
                    <img src="{{ subscription.logo_url }}" alt="{{ subscription.name }}">
                    <div class="details">
                        <h3>{{ subscription.name }}</h3>
                        <div class="amount">{{ subscription.amount|currency }}</div>
                        <div class="cycle">{{ subscription.billing_cycle }}</div>
                    </div>
                    <div class="actions">
                        <a href="{{ url_for('main.edit_subscription', id=subscription.id) }}" class="btn-edit">
                            {{ _('Edit') }}
                        </a>
                    </div>
                </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<!-- Chart.js library -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<!-- Dashboard specific JavaScript -->
<script src="{{ url_for('static', filename='js/dashboard.js') }}"></script>
{% endblock %}
```

### Subscription Forms

#### Add Subscription (add_subscription.html)
Form for adding new subscriptions with the following features:
- File upload for subscription logos
- Dynamic form validation
- Currency selection
- Billing cycle options

```html
{% extends "base.html" %}

{% block title %}{{ _('Add Subscription') }} - {{ _('SubscriptionSage') }}{% endblock %}

{% block styles %}
<!-- Additional styles for forms -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/forms.css') }}">
{% endblock %}

{% block content %}
<div class="form-container">
    <h1>{{ _('Add New Subscription') }}</h1>
    
    <!-- Subscription form -->
    <form method="POST" action="{{ url_for('main.add_subscription') }}" enctype="multipart/form-data" class="subscription-form">
        {{ form.csrf_token }}
        
        <!-- Service name field -->
        <div class="form-group">
            {{ form.name.label }}
            {{ form.name(class="form-control", placeholder=_("Enter service name")) }}
            {% if form.name.errors %}
                <div class="error-message">
                    {% for error in form.name.errors %}
                        {{ error }}
                    {% endfor %}
                </div>
            {% endif %}
        </div>
        
        <!-- Amount field -->
        <div class="form-group">
            {{ form.amount.label }}
            {{ form.amount(class="form-control", placeholder=_("Enter amount")) }}
            {% if form.amount.errors %}
                <div class="error-message">
                    {% for error in form.amount.errors %}
                        {{ error }}
                    {% endfor %}
                </div>
            {% endif %}
        </div>
        
        <!-- Currency field -->
        <div class="form-group">
            {{ form.currency.label }}
            {{ form.currency(class="form-control") }}
            {% if form.currency.errors %}
                <div class="error-message">
                    {% for error in form.currency.errors %}
                        {{ error }}
                    {% endfor %}
                </div>
            {% endif %}
        </div>
        
        <!-- Billing cycle field -->
        <div class="form-group">
            {{ form.billing_cycle.label }}
            {{ form.billing_cycle(class="form-control") }}
            {% if form.billing_cycle.errors %}
                <div class="error-message">
                    {% for error in form.billing_cycle.errors %}
                        {{ error }}
                    {% endfor %}
                </div>
            {% endif %}
        </div>
        
        <!-- Logo upload field -->
        <div class="form-group">
            {{ form.logo.label }}
            {{ form.logo(class="form-control") }}
            {% if form.logo.errors %}
                <div class="error-message">
                    {% for error in form.logo.errors %}
                        {{ error }}
                    {% endfor %}
                </div>
            {% endif %}
        </div>
        
        <!-- Submit button -->
        <div class="form-group">
            <button type="submit" class="btn-primary">{{ _('Add Subscription') }}</button>
            <a href="{{ url_for('main.dashboard') }}" class="btn-secondary">{{ _('Cancel') }}</a>
        </div>
    </form>
</div>
{% endblock %}

{% block scripts %}
<!-- Form validation JavaScript -->
<script src="{{ url_for('static', filename='js/forms.js') }}"></script>
{% endblock %}
```

#### Edit Subscription (edit_subscription.html)
Form for modifying existing subscriptions:
- Pre-populated fields
- Update validation
- Logo management
- Billing cycle modification

### Reports (reports.html)
Detailed financial reports and analytics view:
- Custom date range selection
- Export options
- Data visualization
- Detailed breakdowns

### Authentication Templates

#### Login (login.html)
User authentication form:
- Email/password fields
- Remember me option
- Password reset link
- Registration link

#### Register (register.html)
New user registration form:
- Email validation
- Password requirements
- Terms acceptance
- Welcome message

### Error Pages

#### 404 (404.html)
Custom not found page:
- Clear error message
- Navigation options
- Search functionality

#### 500 (500.html)
Server error page:
- Error details
- Support contact
- Recovery options

## Template Features

### Common Components

1. **Navigation**
   - Responsive menu
   - User profile
   - Quick actions
   - Search bar

2. **Alerts**
   - Success messages
   - Error notifications
   - Warning prompts
   - Info boxes

3. **Modals**
   - Confirmation dialogs
   - Form submissions
   - Quick views
   - Notifications

### Template Variables

1. **User Context**
   ```python
   {
       'user': {
           'id': int,          # Unique user identifier
           'email': str,       # User's email address
           'name': str,        # User's display name
           'preferences': dict # User's application preferences
       }
   }
   ```

2. **Subscription Data**
   ```python
   {
       'subscription': {
           'id': int,                # Unique subscription identifier
           'name': str,              # Name of the subscription service
           'amount': float,          # Subscription cost
           'currency': str,          # Currency code (e.g., USD, EUR)
           'billing_cycle': str,     # Billing frequency (monthly, yearly)
           'next_billing_date': date,# Next payment date
           'logo_url': str           # URL to subscription logo
       }
   }
   ```

### Template Filters

1. **Date Formatting**
   ```jinja2
   {{ date|format_date }}     # Formats date according to user's locale
   {{ date|time_ago }}        # Shows relative time (e.g., "2 days ago")
   ```

2. **Currency Formatting**
   ```jinja2
   {{ amount|format_currency }}           # Formats amount with currency symbol
   {{ amount|convert_currency(to='USD') }}# Converts amount to specified currency
   ```

3. **Text Formatting**
   ```jinja2
   {{ text|truncate(100) }}   # Truncates text to 100 characters with ellipsis
   {{ text|markdown }}        # Renders markdown text as HTML
   ```

## Best Practices

1. **Template Organization**
   - Use template inheritance
   - Keep templates modular
   - Separate concerns
   - Use includes for common elements

2. **Internationalization**
   - Use translation functions
   - Support multiple languages
   - Handle date/time formats
   - Support RTL languages

3. **Accessibility**
   - Use semantic HTML
   - Add ARIA attributes
   - Ensure keyboard navigation
   - Provide alt text

4. **Performance**
   - Minimize template nesting
   - Use efficient loops
   - Cache static content
   - Optimize assets

5. **Security**
   - Escape user input
   - Use CSRF protection
   - Validate form data
   - Secure file uploads 