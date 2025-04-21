import hashlib

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from website.models import add_user, get_user_by_email

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
        if request.method == 'POST':
            email = request.form['email']
            password = hashlib.sha256(request.form['password'].encode()).hexdigest()
            user = get_user_by_email(email)

            if user and user['password'] == password:
                session['user'] = dict(user)
                session['user_id'] = user['id']       # <-- Add this
                session['user_name'] = user['name']   # <-- And this
                return redirect(url_for('views.profile'))

            flash('Invalid email or password.')
        return render_template('login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        try:
            add_user(name, email, password, phone)
            flash('Account created. Please log in.')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash('Email already exists.')
            print(e)
    return render_template('signup.html')

@auth.route('/logout')
def logout():
        session.clear()  # Clears all keys like user_id, user_name, etc.
        return redirect(url_for('auth.login'))

