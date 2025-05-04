# SubscriptionSage Style Guide

This document outlines the coding standards and best practices for the SubscriptionSage project.

## Python Code Style

### General Rules

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guide
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 88 characters (Black formatter default)
- Use meaningful variable and function names
- Write docstrings for all public functions, classes, and modules

### Naming Conventions

- **Variables and Functions**: Use `snake_case`
  ```python
  def calculate_total_cost():
      subscription_price = 9.99
  ```

- **Classes**: Use `PascalCase`
  ```python
  class SubscriptionManager:
      pass
  ```

- **Constants**: Use `UPPER_SNAKE_CASE`
  ```python
  MAX_RETRY_ATTEMPTS = 3
  DEFAULT_CURRENCY = "USD"
  ```

### Imports

- Group imports in the following order:
  1. Standard library imports
  2. Third-party imports
  3. Local application imports
- Sort imports alphabetically within groups
- Use absolute imports

```python
# Standard library
import datetime
import os
from typing import List, Optional

# Third-party
from flask import Flask, request
from sqlalchemy import Column, Integer

# Local
from models import User
from utils import format_currency
```

### Type Hints

- Use type hints for function parameters and return values
- Use `Optional` for parameters that can be `None`
- Use `List`, `Dict`, etc. from `typing` module

```python
from typing import List, Optional

def get_user_subscriptions(user_id: int) -> List[Subscription]:
    pass

def update_subscription(sub_id: int, price: Optional[float] = None) -> bool:
    pass
```

## Flask-Specific Guidelines

### Route Organization

- Group related routes together
- Use descriptive route names
- Follow RESTful conventions where appropriate

```python
# Good
@app.route('/subscriptions', methods=['GET'])
def list_subscriptions():
    pass

@app.route('/subscriptions/<int:sub_id>', methods=['GET'])
def get_subscription(sub_id):
    pass

# Avoid
@app.route('/get_sub', methods=['GET'])
def get_sub():
    pass
```

### Template Organization

- Keep templates in the `templates/` directory
- Use template inheritance with base templates
- Name template files in `snake_case.html`
- Use meaningful block names

```html
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>

<!-- subscription_list.html -->
{% extends "base.html" %}

{% block title %}My Subscriptions{% endblock %}

{% block content %}
    <!-- Content here -->
{% endblock %}
```

## SQLAlchemy Models

### Model Organization

- One model per file in the `models/` directory
- Use descriptive model names
- Include proper relationships and constraints

```python
class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='subscriptions')
```

## JavaScript Style

### General Rules

- Use ES6+ features
- Use meaningful variable and function names
- Use `const` and `let` instead of `var`
- Use arrow functions for callbacks

```javascript
// Good
const calculateTotal = (subscriptions) => {
    return subscriptions.reduce((sum, sub) => sum + sub.price, 0);
};

// Avoid
var total = 0;
for (var i = 0; i < subs.length; i++) {
    total += subs[i].price;
}
```

### Event Handlers

- Use descriptive handler names
- Keep handlers focused and small
- Use event delegation where appropriate

```javascript
// Good
document.querySelector('.subscription-list').addEventListener('click', (e) => {
    if (e.target.matches('.delete-btn')) {
        handleDelete(e.target.dataset.id);
    }
});
```

## CSS Style

### Organization

- Use BEM (Block Element Modifier) naming convention
- Group related styles together
- Use CSS variables for common values

```css
/* Good */
.subscription-card {
    padding: 1rem;
    border-radius: 4px;
}

.subscription-card__title {
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
}

.subscription-card--active {
    border: 2px solid var(--color-success);
}
```

## Git Workflow

### Branch Naming

- Feature branches: `feature/description`
- Bug fixes: `fix/description`
- Documentation: `docs/description`
- Hotfixes: `hotfix/description`

### Commit Messages

- Use present tense
- Start with a verb
- Keep first line under 50 characters
- Use body for detailed explanation

```
feat: add subscription import functionality

- Add CSV import support
- Validate imported data
- Handle duplicate entries
```

## Testing

### Test Organization

- One test file per module
- Name test files with `test_` prefix
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)

```python
def test_calculate_monthly_total():
    # Arrange
    subscriptions = [
        Subscription(price=10.0),
        Subscription(price=15.0)
    ]
    
    # Act
    total = calculate_monthly_total(subscriptions)
    
    # Assert
    assert total == 25.0
```

## Documentation

### Code Comments

- Write comments for complex logic
- Keep comments up to date
- Use docstrings for public APIs
- Avoid obvious comments

```python
# Good
def calculate_prorated_refund(days_remaining: int, monthly_price: float) -> float:
    """
    Calculate prorated refund for subscription cancellation.
    
    Args:
        days_remaining: Number of days left in billing period
        monthly_price: Monthly subscription price
        
    Returns:
        Prorated refund amount
    """
    return (days_remaining / 30) * monthly_price

# Avoid
# This function adds two numbers
def add(a, b):
    return a + b
```

## Security Guidelines

- Never commit sensitive data (passwords, API keys)
- Use environment variables for configuration
- Validate and sanitize all user input
- Use parameterized queries for database operations
- Implement proper authentication and authorization
- Keep dependencies up to date

## Performance Guidelines

- Optimize database queries
- Use appropriate indexes
- Implement caching where beneficial
- Minimize HTTP requests
- Optimize asset loading
- Use pagination for large datasets 