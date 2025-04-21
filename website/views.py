import sqlite3
# in your views.py or wherever your route functions are defined
from flask import Blueprint

views = Blueprint('views', __name__)

@views.route('/admin/another_signup', methods=['GET', 'POST'])
def admin_signup_another():  # Renamed to avoid conflict
    # Logic for another signup or similar functionality
    pass
import hashlib

from flask import Blueprint, redirect, render_template, request, session, url_for, flash

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/search')
def search():
    # Example: getting dummy search results from query params
    location = request.args.get('location')
    checkin = request.args.get('checkin')
    checkout = request.args.get('checkout')

    # Sample dummy data (in a real app you'd query your database)
    hotels = []
    if location and location.lower() == "new york":
        # Use the check-in date for filtering here
        hotels = [
            {'id': 1, 'name': 'Grand Plaza', 'city': 'New York'},
            {'id': 2, 'name': 'Times Square Inn', 'city': 'New York'}
        ]
    return render_template('search.html', hotels=hotels)

@views.route('/profile')
def profile():
    user = session.get('user')
    if not user:
        return redirect(url_for('auth.login'))
    return render_template('profile.html', user=user)

@views.route('/earn-points')
def earn_points():
    if 'user_id' not in session:
        return redirect('/login')

    message = request.args.get('message', '')
    return render_template('earn_points.html', message=message)

@views.route('/redeem-points')
def redeem_points():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT points FROM users WHERE id = ?", (user_id,))
    result = cur.fetchone()
    points = result[0] if result else 0
    conn.close()

    return render_template('redeem_points.html', points=points)

@views.route('/payment-methods')
def payment_methods():
    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS payment_methods
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER,
                   card_name TEXT,
                   last_four TEXT,
                   expiry TEXT)''')

    cur.execute("SELECT id, card_name, last_four, expiry FROM payment_methods WHERE user_id = ?", 
                (session['user_id'],))
    payment_methods = cur.fetchall()
    conn.close()

    return render_template('payment_methods.html', payment_methods=payment_methods)

@views.route('/add-payment-method', methods=['POST'])
def add_payment_method():
    if 'user_id' not in session:
        return redirect('/login')

    card_name = request.form['card_name']
    card_number = request.form['card_number']
    expiry = request.form['expiry']

    # Only store last 4 digits for security
    last_four = card_number[-4:] if len(card_number) >= 4 else card_number

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('''INSERT INTO payment_methods (user_id, card_name, last_four, expiry)
                   VALUES (?, ?, ?, ?)''', 
                (session['user_id'], card_name, last_four, expiry))
    conn.commit()
    conn.close()

    return redirect('/payment-methods')

@views.route('/delete-payment-method/<int:method_id>')
def delete_payment_method(method_id):
    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM payment_methods WHERE id = ? AND user_id = ?", 
                (method_id, session['user_id']))
    conn.commit()
    conn.close()

    return redirect('/payment-methods')

@views.route('/personal-details')
def personal_details():
    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT name, email, phone FROM users WHERE id = ?", (session['user_id'],))
    user = cur.fetchone()
    conn.close()

    return render_template('personal_details.html', user=user)

@views.route('/update-personal-details', methods=['POST'])
def update_personal_details():
    if 'user_id' not in session:
        return redirect('/login')

    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("UPDATE users SET name = ?, email = ?, phone = ? WHERE id = ?", 
                (name, email, phone, session['user_id']))
    conn.commit()
    conn.close()

    return redirect('/personal-details')

@views.route('/booking-history')
def booking_history():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('booking_history.html')

@views.route('/manage-bookings')
def manage_bookings():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('manage_bookings.html')

@views.route('/packages')
def packages():
    return redirect('/#packages')

@views.route('/reviews')
def reviews():
    return redirect('/#reviews')

@views.route('/referrals')
def referrals():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('referrals.html')

@views.route('/wishlist')
def wishlist():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('wishlist.html')

@views.route('/favorites')
def favorites():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('favorites.html')

@views.route('/notifications')
def notifications():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('notifications.html')

@views.route('/settings')
def settings():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('settings.html')

@views.route('/help')
def help():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('help.html')

@views.route('/feedback')
def feedback():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('feedback.html')

@views.route('/contact')
def contact():
    return redirect('/#contact')

@views.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        email = request.form['email']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()

        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS admin_users 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       email TEXT UNIQUE,
                       password TEXT)''')
        try:
            cur.execute("INSERT INTO admin_users (email, password) VALUES (?, ?)", 
                       (email, password))
            conn.commit()
            flash('Account created successfully')
            return redirect('/admin/login')
        except sqlite3.IntegrityError:
            flash('Email already exists')
        except Exception as e:
            flash('An error occurred during registration')
            print(e)
        finally:
            conn.close()

    return render_template('admin_signup.html')

@views.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM admin_users WHERE email = ? AND password = ?", 
                   (email, hashlib.sha256(password.encode()).hexdigest()))
        admin = cur.fetchone()
        conn.close()

        if admin:
            session['admin_id'] = admin[0]
            session['admin_email'] = admin[1]
            return redirect('/admin/dashboard')
        flash('Invalid credentials')
        return redirect('/admin/signup')

    return render_template('admin_login.html')