# Frontend Assets Documentation

## Static Assets

### CSS Structure
Located in `static/css/`

```css
/* main.css - Core application styles */
:root {
    /* Color variables for consistent theming */
    --primary-color: #4a90e2;      /* Main brand color */
    --secondary-color: #2c3e50;    /* Secondary brand color */
    --text-color: #333333;         /* Main text color */
    --background-color: #ffffff;    /* Background color */
    --error-color: #e74c3c;        /* Error message color */
    --success-color: #2ecc71;      /* Success message color */
}

/* Global styles */
body {
    font-family: 'Inter', sans-serif;  /* Modern, readable font */
    line-height: 1.6;                  /* Comfortable line spacing */
    color: var(--text-color);          /* Use CSS variable for text color */
    background: var(--background-color); /* Use CSS variable for background */
}

/* Component styles */
.card {
    border-radius: 8px;              /* Rounded corners */
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);  /* Subtle shadow */
    padding: 1.5rem;                 /* Internal spacing */
    margin-bottom: 1rem;             /* Space between cards */
}

/* Form styles */
.form-group {
    margin-bottom: 1rem;             /* Space between form elements */
}

.form-control {
    width: 100%;                     /* Full width inputs */
    padding: 0.5rem;                 /* Comfortable input padding */
    border: 1px solid #ddd;          /* Light border */
    border-radius: 4px;              /* Slightly rounded corners */
}
```

Key Features:
- CSS variables for theming
- Responsive design patterns
- Component-based styling
- Form styling utilities

### JavaScript Structure
Located in `static/js/`

```javascript
// main.js - Core application functionality
document.addEventListener('DOMContentLoaded', () => {
    // Initialize application components
    initializeNavigation();    // Set up navigation
    initializeForms();        // Set up form handling
    initializeNotifications(); // Set up notifications
});

// Navigation handling
function initializeNavigation() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    // Toggle mobile navigation
    navToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');  // Toggle active class
    });
    
    // Handle navigation links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            // Add active state to current page
            document.querySelectorAll('.nav-link').forEach(l => 
                l.classList.remove('active'));
            e.target.classList.add('active');
        });
    });
}

// Form handling
function initializeForms() {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();  // Prevent default form submission
            
            // Validate form data
            if (!validateForm(form)) {
                return;  // Stop if validation fails
            }
            
            try {
                // Submit form data
                const response = await submitForm(form);
                handleFormResponse(response);
            } catch (error) {
                showError(error.message);
            }
        });
    });
}

// API integration
async function submitForm(form) {
    const formData = new FormData(form);  // Get form data
    const data = Object.fromEntries(formData);  // Convert to object
    
    // Send API request
    const response = await fetch(form.action, {
        method: form.method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getAuthToken()}`  // Add auth token
        },
        body: JSON.stringify(data)
    });
    
    return response.json();  // Return response data
}
```

Key Features:
- Event handling
- Form validation
- API integration
- Error handling

### Uploads Directory
Located in `static/uploads/`

```python
# uploads/__init__.py - Upload handling configuration
UPLOAD_CONFIG = {
    'allowed_extensions': {  # Allowed file types
        'images': ['.jpg', '.jpeg', '.png', '.gif'],
        'documents': ['.pdf', '.doc', '.docx']
    },
    'max_file_size': 5 * 1024 * 1024,  # 5MB max file size
    'storage_paths': {  # Storage locations
        'logos': 'static/uploads/logos/',
        'avatars': 'static/uploads/avatars/',
        'temp': 'static/uploads/temp/'
    }
}

# File handling functions
def validate_upload(file, file_type):
    """Validate uploaded file"""
    # Check file extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in UPLOAD_CONFIG['allowed_extensions'][file_type]:
        raise ValueError('Invalid file type')
    
    # Check file size
    if file.content_length > UPLOAD_CONFIG['max_file_size']:
        raise ValueError('File too large')
    
    return True

def save_upload(file, file_type, filename):
    """Save uploaded file"""
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}_{filename}"
    save_path = os.path.join(
        UPLOAD_CONFIG['storage_paths'][file_type],
        unique_filename
    )
    
    # Save file
    file.save(save_path)
    return unique_filename
```

Key Features:
- File type validation
- Size restrictions
- Secure storage
- Unique filenames

### Localization
Located in `static/locales/`

```javascript
// locales/en.json - English translations
{
    "common": {
        "save": "Save",
        "cancel": "Cancel",
        "delete": "Delete",
        "edit": "Edit"
    },
    "auth": {
        "login": "Login",
        "register": "Register",
        "logout": "Logout",
        "email": "Email",
        "password": "Password"
    },
    "subscriptions": {
        "add": "Add Subscription",
        "edit": "Edit Subscription",
        "delete": "Delete Subscription",
        "name": "Subscription Name",
        "amount": "Amount",
        "currency": "Currency",
        "billing_cycle": "Billing Cycle"
    },
    "errors": {
        "required": "This field is required",
        "invalid_email": "Invalid email format",
        "password_too_short": "Password must be at least 8 characters"
    }
}

// Localization handling
function initializeLocalization() {
    // Load user's preferred language
    const userLang = getUserLanguage();
    loadTranslations(userLang);
    
    // Update UI with translations
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        element.textContent = getTranslation(key);
    });
}

async function loadTranslations(lang) {
    try {
        // Load translation file
        const response = await fetch(`/static/locales/${lang}.json`);
        translations = await response.json();
        
        // Update UI
        updateUITranslations();
    } catch (error) {
        console.error('Failed to load translations:', error);
        // Fallback to default language
        loadTranslations('en');
    }
}
```

Key Features:
- JSON-based translations
- Dynamic loading
- Fallback handling
- UI updates

## Email Templates

### Authentication Emails
Located in `templates/email/`

```html
<!-- welcome.html - New user welcome email -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to SubscriptionSage</title>
    <style>
        /* Email styles */
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            padding: 20px 0;
        }
        .content {
            padding: 20px;
            background: #f9f9f9;
            border-radius: 5px;
        }
        .button {
            display: inline-block;
            padding: 10px 20px;
            background: #4a90e2;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="header">
        <img src="{{ logo_url }}" alt="SubscriptionSage Logo">
    </div>
    <div class="content">
        <h1>Welcome to SubscriptionSage!</h1>
        <p>Hello {{ user.name }},</p>
        <p>Thank you for joining SubscriptionSage. We're excited to help you manage your subscriptions effectively.</p>
        <a href="{{ verification_url }}" class="button">Verify Your Email</a>
        <p>If you didn't create this account, please ignore this email.</p>
    </div>
</body>
</html>
```

Key Features:
- Responsive design
- Brand consistency
- Clear call-to-action
- Fallback content

### Notification Emails
Located in `templates/email/`

```html
# Notification templates:
- subscription_renewal.html    # Upcoming renewal
- payment_reminder.html        # Payment due
- subscription_expired.html    # Expired subscription
```

Key Features:
- Important information highlighting
- Action buttons
- Summary sections
- Personalization

### Report Emails
Located in `templates/email/`

```html
# Report templates:
- monthly_summary.html     # Monthly spending report
- yearly_summary.html      # Yearly spending report
- custom_report.html       # Custom period report
```

Key Features:
- Data visualization
- Summary tables
- Export options
- Customization

## Best Practices

1. **Asset Organization**
   - Clear directory structure
   - Consistent naming
   - Version control
   - Dependency management

2. **Performance**
   - Asset minification
   - Image optimization
   - Lazy loading
   - Caching strategies

3. **Accessibility**
   - Alt text for images
   - ARIA labels
   - Keyboard navigation
   - Screen reader support

4. **Security**
   - File validation
   - Access control
   - Content security
   - XSS prevention

5. **Maintenance**
   - Regular updates
   - Version tracking
   - Backup strategy
   - Cleanup procedures 