import os
import csv
import io
import logging
from datetime import datetime, timedelta
from flask import render_template, flash, redirect, url_for, request, jsonify, send_file
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import urlsplit
from app import app, db
from models import User, Subscription, Reminder, ExchangeRate
from utils import convert_currency, fetch_exchange_rates, send_reminder_email
import pandas as pd

# Default subscriptions to populate
DEFAULT_SUBSCRIPTIONS = [
    {"name": "Apple TV", "url": "https://www.apple.com/apple-tv-plus/"},
    {"name": "Bolt", "url": "https://bolt.new/"},
    {"name": "Cursor", "url": "https://cursor.sh/"},
    {"name": "GitHub", "url": "https://github.com/"},
    {"name": "GitLab", "url": "https://gitlab.com/"},
    {"name": "Granola", "url": "https://granola.ai/"},
    {"name": "Linear", "url": "https://linear.app/"},
    {"name": "Lovable", "url": "https://lovable.dev/"},
    {"name": "Netflix", "url": "https://www.netflix.com/"},
    {"name": "Notability", "url": "https://notability.com/"},
    {"name": "Notion", "url": "https://www.notion.so/"},
    {"name": "Perplexity AI", "url": "https://www.perplexity.ai/"},
    {"name": "Replit", "url": "https://replit.com/"},
    {"name": "Superhuman", "url": "https://superhuman.com/"},
    {"name": "Todoist", "url": "https://todoist.com/"},
    {"name": "v0", "url": "https://v0.dev/"},
    {"name": "YouTube Premium", "url": "https://www.youtube.com/premium"}
]

# Home page
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

# User authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        
        login_user(user, remember=True)
        
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('dashboard')
            
        return redirect(next_page)
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        language = request.form.get('language', 'en')
        preferred_currency = request.form.get('preferred_currency', 'USD')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email, language=language, preferred_currency=preferred_currency)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Set up default reminders
        create_default_reminders(user)
        
        flash('Registration successful, please log in', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    subscriptions = Subscription.query.filter_by(user_id=current_user.id).all()
    
    # Calculate next payment date for each subscription
    for sub in subscriptions:
        sub.calculate_next_payment_date()
    
    # Get upcoming payments
    upcoming_payments = Subscription.query.filter(
        Subscription.user_id == current_user.id,
        Subscription.next_payment_date.isnot(None),
        Subscription.next_payment_date > datetime.utcnow(),
        Subscription.is_active == True
    ).order_by(Subscription.next_payment_date).limit(5).all()
    
    # Get monthly spending
    monthly_spending = 0
    for sub in subscriptions:
        if sub.is_active and sub.billing_cycle != 'lifetime':
            amount_in_preferred = convert_currency(
                sub.amount,
                sub.currency,
                current_user.preferred_currency
            )
            
            if sub.billing_cycle == 'weekly':
                monthly_spending += amount_in_preferred * 4.33  # Average weeks in a month
            elif sub.billing_cycle == 'monthly':
                monthly_spending += amount_in_preferred
            elif sub.billing_cycle == 'quarterly':
                monthly_spending += amount_in_preferred / 3
            elif sub.billing_cycle == 'bi-annually':
                monthly_spending += amount_in_preferred / 6
            elif sub.billing_cycle == 'yearly':
                monthly_spending += amount_in_preferred / 12
    
    # Total number of subscriptions
    total_subscriptions = len(subscriptions)
    active_subscriptions = sum(1 for sub in subscriptions if sub.is_active)
    
    # Get subscription counts by billing cycle for chart
    billing_cycles = ['weekly', 'monthly', 'quarterly', 'bi-annually', 'yearly', 'lifetime']
    cycle_counts = {}
    for cycle in billing_cycles:
        cycle_counts[cycle] = sum(1 for sub in subscriptions if sub.billing_cycle == cycle and sub.is_active)
    
    # Pass current time to template
    current_datetime = datetime.now()
    
    return render_template(
        'dashboard.html',
        subscriptions=subscriptions,
        upcoming_payments=upcoming_payments,
        monthly_spending=monthly_spending,
        total_subscriptions=total_subscriptions,
        active_subscriptions=active_subscriptions,
        cycle_counts=cycle_counts,
        current_datetime=current_datetime
    )

# Subscription management
@app.route('/subscriptions/add', methods=['GET', 'POST'])
@login_required
def add_subscription():
    if request.method == 'POST':
        name = request.form.get('name')
        url = request.form.get('url')
        amount = float(request.form.get('amount', 0))
        currency = request.form.get('currency', 'USD')
        billing_cycle = request.form.get('billing_cycle')
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
        notes = request.form.get('notes')
        enable_reminders = 'enable_reminders' in request.form

        # Handle logo upload
        logo_url = None
        used_temp_id = False
        temp_logo_url = None

        if 'logo' in request.files:
            logo_file = request.files['logo']
            if logo_file and logo_file.filename:
                logo_url = handle_image_upload(logo_file, current_user.id)
                used_temp_id = True
                temp_logo_url = logo_url

        subscription = Subscription(
            user_id=current_user.id,
            name=name,
            url=url,
            logo_url=logo_url,
            amount=amount,
            currency=currency,
            billing_cycle=billing_cycle,
            start_date=start_date,
            notes=notes
        )
        
        # Calculate next payment date
        subscription.calculate_next_payment_date()
        
        db.session.add(subscription)
        db.session.commit()
        
        # If we used a temporary ID for the logo upload, we need to rename the file
        # with the actual subscription ID and update the logo_url
        if used_temp_id and temp_logo_url:
            import os
            from utils import handle_image_upload
            
            # Get the original file path
            temp_file_path = temp_logo_url[1:]  # Remove leading slash
            
            if os.path.exists(temp_file_path):
                # Get file extension
                extension = os.path.splitext(temp_file_path)[1]
                
                # Create new filename with actual subscription ID
                new_filename = f"{subscription.id}_{os.path.basename(temp_file_path).split('_', 1)[1]}"
                new_path = os.path.join('static', 'uploads', new_filename)
                
                # Rename file
                try:
                    os.rename(temp_file_path, new_path)
                    subscription.logo_url = f"/{new_path}"
                    db.session.commit()
                except Exception as e:
                    logging.error(f"Error renaming temp logo file: {str(e)}")
        
        # Create reminders only if enabled
        if enable_reminders and subscription.billing_cycle != 'lifetime':
            create_subscription_reminders(subscription)
        
        # Commit all changes
        db.session.commit()
        
        flash('Subscription added successfully', 'success')
        return redirect(url_for('dashboard'))
    
    # Get suggested subscriptions
    suggested_subscriptions = DEFAULT_SUBSCRIPTIONS.copy()
    
    # Add logo URLs to suggested subscriptions
    from utils import get_logo_url_for_service
    for sub in suggested_subscriptions:
        sub['logo_url'] = get_logo_url_for_service(sub['name'], sub['url'])
    
    # Pass today's date for the start_date field
    today = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('add_subscription.html', 
                          suggested_subscriptions=suggested_subscriptions,
                          today=today)

@app.route('/subscriptions/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_subscription(id):
    subscription = Subscription.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    reminders = Reminder.query.filter_by(subscription_id=id).all()
    
    if request.method == 'POST':
        subscription.name = request.form.get('name')
        subscription.url = request.form.get('url')
        subscription.amount = float(request.form.get('amount', 0))
        subscription.currency = request.form.get('currency', 'USD')
        subscription.billing_cycle = request.form.get('billing_cycle')
        subscription.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
        subscription.notes = request.form.get('notes')
        subscription.is_active = 'is_active' in request.form
        enable_reminders = 'enable_reminders' in request.form

        # Handle logo upload
        if 'logo' in request.files:
            logo_file = request.files['logo']
            if logo_file and logo_file.filename:
                # Delete old logo if exists
                if subscription.logo_url:
                    try:
                        os.remove(subscription.logo_url[1:])  # Remove leading slash
                    except Exception as e:
                        logging.error(f"Error deleting old logo: {str(e)}")
                
                # Upload new logo
                subscription.logo_url = handle_image_upload(logo_file, current_user.id)

        # Handle logo removal
        if 'remove_logo' in request.form and subscription.logo_url:
            try:
                os.remove(subscription.logo_url[1:])  # Remove leading slash
                subscription.logo_url = None
            except Exception as e:
                logging.error(f"Error deleting logo: {str(e)}")

        # Handle reminders
        if enable_reminders:
            # Delete existing reminders
            for reminder in reminders:
                db.session.delete(reminder)
            
            # Add new reminders (max 3)
            reminder_count = min(int(request.form.get('reminder_count', 0)), 3)
            
            for i in range(1, reminder_count + 1):
                days_before = int(request.form.get(f'days_before_{i}', 7))
                email_notification = f'email_notification_{i}' in request.form
                push_notification = f'push_notification_{i}' in request.form
                
                reminder = Reminder(
                    user_id=current_user.id,
                    subscription_id=id,
                    days_before=days_before,
                    email_notification=email_notification,
                    push_notification=push_notification
                )
                
                db.session.add(reminder)
        else:
            # Delete all reminders if disabled
            for reminder in reminders:
                db.session.delete(reminder)
        
        db.session.commit()
        flash('Subscription updated successfully', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_subscription.html', subscription=subscription, reminders=reminders)

@app.route('/subscriptions/delete/<int:id>', methods=['POST'])
@login_required
def delete_subscription(id):
    subscription = Subscription.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    db.session.delete(subscription)
    db.session.commit()
    
    flash('Subscription deleted successfully', 'success')
    return redirect(url_for('dashboard'))

# Reminders management
@app.route('/reminders/<int:subscription_id>', methods=['GET', 'POST'])
@login_required
def manage_reminders(subscription_id):
    subscription = Subscription.query.filter_by(id=subscription_id, user_id=current_user.id).first_or_404()
    reminders = Reminder.query.filter_by(subscription_id=subscription_id).all()
    
    if request.method == 'POST':
        # Delete existing reminders
        for reminder in reminders:
            db.session.delete(reminder)
        
        # Add new reminders (max 3)
        reminder_count = min(int(request.form.get('reminder_count', 0)), 3)
        
        for i in range(1, reminder_count + 1):
            days_before = int(request.form.get(f'days_before_{i}', 7))
            email_notification = f'email_notification_{i}' in request.form
            push_notification = f'push_notification_{i}' in request.form
            
            reminder = Reminder(
                user_id=current_user.id,
                subscription_id=subscription_id,
                days_before=days_before,
                email_notification=email_notification,
                push_notification=push_notification
            )
            
            db.session.add(reminder)
        
        db.session.commit()
        flash('Reminders updated successfully', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_subscription.html', subscription=subscription, reminders=reminders)

# Reports
@app.route('/reports')
@login_required
def reports():
    subscriptions = Subscription.query.filter_by(user_id=current_user.id).all()
    
    # Calculate monthly spending by category
    billing_cycles = ['weekly', 'monthly', 'quarterly', 'bi-annually', 'yearly']
    spending_by_cycle = {cycle: 0 for cycle in billing_cycles}
    
    # Add converted amounts to each subscription for display in the template
    for sub in subscriptions:
        # Add the amount in user's preferred currency as a property
        sub.amount_in_preferred = convert_currency(
            sub.amount,
            sub.currency,
            current_user.preferred_currency
        )
        
        # Calculate monthly and yearly costs in preferred currency
        if sub.billing_cycle == 'weekly':
            sub.monthly_cost = sub.amount_in_preferred * 4.33  # Average weeks in a month
            sub.yearly_cost = sub.amount_in_preferred * 52
        elif sub.billing_cycle == 'monthly':
            sub.monthly_cost = sub.amount_in_preferred
            sub.yearly_cost = sub.amount_in_preferred * 12
        elif sub.billing_cycle == 'quarterly':
            sub.monthly_cost = sub.amount_in_preferred / 3
            sub.yearly_cost = sub.amount_in_preferred * 4
        elif sub.billing_cycle == 'bi-annually':
            sub.monthly_cost = sub.amount_in_preferred / 6
            sub.yearly_cost = sub.amount_in_preferred * 2
        elif sub.billing_cycle == 'yearly':
            sub.monthly_cost = sub.amount_in_preferred / 12
            sub.yearly_cost = sub.amount_in_preferred
        else:  # lifetime
            sub.monthly_cost = 0
            sub.yearly_cost = 0
        
        # Update spending by cycle for the chart
        if sub.is_active and sub.billing_cycle != 'lifetime':
            if sub.billing_cycle == 'weekly':
                spending_by_cycle['weekly'] += sub.monthly_cost
            elif sub.billing_cycle == 'monthly':
                spending_by_cycle['monthly'] += sub.monthly_cost
            elif sub.billing_cycle == 'quarterly':
                spending_by_cycle['quarterly'] += sub.monthly_cost
            elif sub.billing_cycle == 'bi-annually':
                spending_by_cycle['bi-annually'] += sub.monthly_cost
            elif sub.billing_cycle == 'yearly':
                spending_by_cycle['yearly'] += sub.monthly_cost
    
    # Get upcoming payments in the next 30 days
    now = datetime.utcnow()
    next_month = now + timedelta(days=30)
    
    upcoming_payments = Subscription.query.filter(
        Subscription.user_id == current_user.id,
        Subscription.next_payment_date.isnot(None),
        Subscription.next_payment_date.between(now, next_month),
        Subscription.is_active == True
    ).order_by(Subscription.next_payment_date).all()
    
    # Also add converted amounts to upcoming payments
    for payment in upcoming_payments:
        payment.amount_in_preferred = convert_currency(
            payment.amount,
            payment.currency,
            current_user.preferred_currency
        )
    
    # Calculate totals
    total_monthly = sum(spending_by_cycle.values())
    total_yearly = total_monthly * 12
    
    # Pass current time to template
    current_datetime = datetime.now()
    
    return render_template(
        'reports.html',
        subscriptions=subscriptions,
        spending_by_cycle=spending_by_cycle,
        upcoming_payments=upcoming_payments,
        total_monthly=total_monthly,
        total_yearly=total_yearly,
        current_datetime=current_datetime
    )

# CSV import/export
@app.route('/export_csv')
@login_required
def export_csv():
    subscriptions = Subscription.query.filter_by(user_id=current_user.id).all()
    
    csv_data = []
    for sub in subscriptions:
        # Get reminders for this subscription
        reminders = []
        for reminder in sub.reminders:
            reminders.append(f"{reminder.days_before} days (Email: {reminder.email_notification}, Push: {reminder.push_notification})")
        
        csv_data.append({
            'Name': sub.name,
            'URL': sub.url,
            'Logo URL': sub.logo_url or '',
            'Amount': sub.amount,
            'Currency': sub.currency,
            'Billing Cycle': sub.billing_cycle,
            'Start Date': sub.start_date.strftime('%Y-%m-%d'),
            'Next Payment Date': sub.next_payment_date.strftime('%Y-%m-%d') if sub.next_payment_date else '',
            'Notes': sub.notes,
            'Active': 'Yes' if sub.is_active else 'No',
            'Created At': sub.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'Updated At': sub.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'Reminders': '; '.join(reminders) if reminders else ''
        })
    
    # Create a CSV in memory
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=csv_data[0].keys() if csv_data else [])
    writer.writeheader()
    writer.writerows(csv_data)
    
    # Create the response
    mem_file = io.BytesIO()
    mem_file.write(output.getvalue().encode('utf-8'))
    mem_file.seek(0)
    
    return send_file(
        mem_file,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'subscriptions_{datetime.now().strftime("%Y%m%d")}.csv'
    )

@app.route('/import_csv', methods=['POST'])
@login_required
def import_csv():
    if 'csv_file' not in request.files:
        flash('No file selected', 'danger')
        return redirect(url_for('dashboard'))
    
    file = request.files['csv_file']
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(url_for('dashboard'))
    
    if not file.filename.endswith('.csv'):
        flash('Please upload a CSV file', 'danger')
        return redirect(url_for('dashboard'))
    
    try:
        # Read CSV file
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_data = csv.DictReader(stream)
        
        for row in csv_data:
            name = row['Name']
            url = row.get('URL', '')
            logo_url = row.get('Logo URL', '')  # Get logo URL if it exists
            amount = float(row.get('Amount', 0))
            currency = row.get('Currency', 'USD')
            billing_cycle = row.get('Billing Cycle', 'monthly')
            start_date_str = row.get('Start Date', datetime.utcnow().strftime('%Y-%m-%d'))
            notes = row.get('Notes', '')
            is_active = row.get('Active', 'Yes') == 'Yes'
            
            # Parse start date
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            except ValueError:
                start_date = datetime.utcnow()
            
            # Check if subscription already exists (by name)
            existing_sub = Subscription.query.filter_by(
                user_id=current_user.id,
                name=name
            ).first()
            
            if existing_sub:
                # Update existing subscription
                existing_sub.url = url
                # Update logo_url if provided in CSV, otherwise keep existing
                if logo_url:
                    existing_sub.logo_url = logo_url
                existing_sub.amount = amount
                existing_sub.currency = currency
                existing_sub.billing_cycle = billing_cycle
                existing_sub.start_date = start_date
                existing_sub.notes = notes
                existing_sub.is_active = is_active
                existing_sub.calculate_next_payment_date()
                
                # Clear existing reminders
                for reminder in existing_sub.reminders:
                    db.session.delete(reminder)
            else:
                # Create new subscription
                from utils import get_logo_url_for_service
                if not logo_url:
                    logo_url = get_logo_url_for_service(name, url)
                
                subscription = Subscription(
                    user_id=current_user.id,
                    name=name,
                    url=url,
                    logo_url=logo_url,
                    amount=amount,
                    currency=currency,
                    billing_cycle=billing_cycle,
                    start_date=start_date,
                    notes=notes,
                    is_active=is_active
                )
                
                subscription.calculate_next_payment_date()
                db.session.add(subscription)
                
                # Need to flush to get the ID before creating reminders
                db.session.flush()
            
            # Process reminders if provided
            if 'Reminders' in row and row['Reminders']:
                reminder_strings = row['Reminders'].split(';')
                for reminder_str in reminder_strings:
                    try:
                        # Parse reminder string (e.g., "7 days (Email: True, Push: False)")
                        days = int(reminder_str.split(' days')[0])
                        email = 'Email: True' in reminder_str
                        push = 'Push: True' in reminder_str
                        
                        reminder = Reminder(
                            user_id=current_user.id,
                            subscription_id=existing_sub.id if existing_sub else subscription.id,
                            days_before=days,
                            email_notification=email,
                            push_notification=push
                        )
                        db.session.add(reminder)
                    except (ValueError, IndexError):
                        continue
            elif not existing_sub and subscription.billing_cycle != 'lifetime':
                # Create default reminders for new subscription
                default_days = [1, 7, 14]
                for days in default_days:
                    reminder = Reminder(
                        user_id=current_user.id,
                        subscription_id=subscription.id,
                        days_before=days,
                        email_notification=True,
                        push_notification=False
                    )
                    db.session.add(reminder)
        
        # Commit all changes if successful
        db.session.commit()
        flash('CSV imported successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error importing CSV: {str(e)}', 'danger')
        logging.error(f"CSV import error: {str(e)}")
    
    return redirect(url_for('dashboard'))

# Settings
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        current_user.language = request.form['language']
        current_user.preferred_currency = request.form['preferred_currency']
        
        # Update password if provided
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if current_password and new_password and confirm_password:
            if not current_user.check_password(current_password):
                flash('Current password is incorrect', 'danger')
                return redirect(url_for('settings'))
            
            if new_password != confirm_password:
                flash('New passwords do not match', 'danger')
                return redirect(url_for('settings'))
            
            current_user.set_password(new_password)
            flash('Password updated successfully', 'success')
        
        db.session.commit()
        flash('Settings updated successfully', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('settings.html')

# API endpoints
@app.route('/api/exchange_rates')
@login_required
def get_exchange_rates():
    currencies = ['USD', 'EUR', 'CZK', 'PLN']
    rates = {}
    
    # Get all exchange rates from the database
    for base in currencies:
        rates[base] = {}
        for target in currencies:
            if base == target:
                rates[base][target] = 1.0
            else:
                exchange_rate = ExchangeRate.query.filter_by(
                    base_currency=base,
                    target_currency=target
                ).first()
                
                if exchange_rate:
                    rates[base][target] = exchange_rate.rate
                else:
                    # If no rate found, try to calculate via USD
                    if base != 'USD' and target != 'USD':
                        base_to_usd = ExchangeRate.query.filter_by(
                            base_currency=base,
                            target_currency='USD'
                        ).first()
                        usd_to_target = ExchangeRate.query.filter_by(
                            base_currency='USD',
                            target_currency=target
                        ).first()
                        
                        if base_to_usd and usd_to_target:
                            rates[base][target] = (1 / base_to_usd.rate) * usd_to_target.rate
                        else:
                            rates[base][target] = 1.0
                    else:
                        rates[base][target] = 1.0
    
    return jsonify(rates)

@app.route('/api/refresh_exchange_rates', methods=['POST'])
@login_required
def refresh_exchange_rates():
    try:
        fetch_exchange_rates()
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error refreshing exchange rates: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/set_exchange_rate_api_key', methods=['POST'])
@login_required
def set_exchange_rate_api_key():
    try:
        data = request.get_json()
        api_key = data.get('api_key')
        
        if not api_key:
            return jsonify({'success': False, 'message': 'API key is required'}), 400
        
        # Store the API key in the database
        user = User.query.get(current_user.id)
        user.exchange_rate_api_key = api_key
        db.session.commit()
        
        # Attempt to fetch exchange rates with the new key
        try:
            fetch_exchange_rates()
            return jsonify({'success': True, 'message': 'API key saved and exchange rates updated successfully'})
        except Exception as e:
            # If fetching fails, rollback the API key
            user.exchange_rate_api_key = None
            db.session.commit()
            return jsonify({'success': False, 'message': f'Invalid API key: {str(e)}'}), 400
            
    except Exception as e:
        logger.error(f"Error setting API key: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/mark_paid/<int:subscription_id>', methods=['POST'])
@login_required
def mark_paid(subscription_id):
    subscription = Subscription.query.filter_by(id=subscription_id, user_id=current_user.id).first_or_404()
    
    # Update the next payment date based on the billing cycle
    if subscription.billing_cycle != 'lifetime':
        subscription.calculate_next_payment_date()
        db.session.commit()
    
    return jsonify({'success': True, 'next_payment_date': subscription.next_payment_date.strftime('%Y-%m-%d') if subscription.next_payment_date else None})

# Helper functions
def create_default_reminders(user):
    """Create default user reminders preferences."""
    # We no longer create default reminders at the user level
    # Default reminders are now created per subscription only
    pass

def create_subscription_reminders(subscription):
    """Create default reminders for a subscription (1, 7, and 14 days before)."""
    if subscription.billing_cycle == 'lifetime':
        return
    
    # Default reminder days
    default_days = [1, 7, 14]
    
    for days in default_days:
        reminder = Reminder(
            user_id=subscription.user_id,
            subscription_id=subscription.id,
            days_before=days,
            email_notification=True,
            push_notification=False
        )
        db.session.add(reminder)
    
    # Note: We don't commit here anymore - let the calling function decide when to commit
    # This solves transaction issues during CSV import and other bulk operations

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
