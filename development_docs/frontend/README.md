# Frontend Documentation

## Overview
The frontend of SubscriptionSage is built using HTML templates with Jinja2 templating engine, CSS for styling, and JavaScript for interactivity. The application follows a responsive design pattern and uses Bootstrap for the UI framework.

## Directory Structure
```
frontend/
├── templates/           # HTML templates
├── static/
│   ├── css/           # Stylesheets
│   ├── js/            # JavaScript files
│   ├── uploads/       # User uploaded files
│   └── locales/       # Localization files
```

## Key Components

### Templates
1. **base.html**
   - Main template that serves as the layout for all pages
   - Contains common elements like navigation, footer, and meta tags
   - Implements responsive design patterns

2. **dashboard.html**
   - Main dashboard view showing subscription overview
   - Implements data visualization and summary statistics
   - Key features:
     - Subscription summary cards
     - Recent activity feed
     - Quick action buttons

3. **add_subscription.html**
   - Form for adding new subscriptions
   - Implements form validation
   - Handles file uploads for subscription logos

4. **edit_subscription.html**
   - Form for modifying existing subscriptions
   - Pre-populated with current subscription data
   - Implements update validation

5. **reports.html**
   - Detailed financial reports and analytics
   - Implements data visualization
   - Export functionality

### Static Assets

#### CSS
- Custom styles complementing Bootstrap
- Responsive design implementations
- Theme customization

#### JavaScript
- Form validation
- Dynamic content updates
- API interactions
- Data visualization

## Key Features
1. **Responsive Design**
   - Mobile-first approach
   - Bootstrap grid system
   - Custom breakpoints

2. **User Interface**
   - Clean, modern design
   - Intuitive navigation
   - Consistent styling

3. **Form Handling**
   - Client-side validation
   - File upload support
   - Dynamic form fields

4. **Data Visualization**
   - Charts and graphs
   - Interactive elements
   - Real-time updates

## Best Practices
1. **Code Organization**
   - Modular template structure
   - Reusable components
   - Clear naming conventions

2. **Performance**
   - Optimized asset loading
   - Minified resources
   - Efficient DOM manipulation

3. **Accessibility**
   - ARIA labels
   - Semantic HTML
   - Keyboard navigation

## Development Guidelines
1. **Template Development**
   - Use Jinja2 inheritance
   - Maintain consistent structure
   - Document complex logic

2. **Styling**
   - Follow BEM methodology
   - Use CSS variables
   - Maintain responsive design

3. **JavaScript**
   - Modular code structure
   - Error handling
   - Performance optimization 