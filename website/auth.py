from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import re

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in sucessfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name= request.form.get('firstName')
        password1= request.form.get('password1')
        password2= request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(first_name) < 1:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords dont\'t match.', category='error')
        elif len(password1) < 8:
            flash('Passwords must have at least 8 characters', category='error')
        elif not password_complexity(password1):
            flash('Password must contain at least 1 uppercase, 1 lowercase, 1 number, and 1 special character. Example: "Passw0rd!"', category='error')
        else:
            new_user= User(email=email, first_name=first_name, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()            
            flash('Account created', category='success')

            return redirect(url_for('auth.login'))

    return render_template("sign_up.html", user=current_user)

def password_complexity(password):
    # Password complexity pattern
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return bool(re.match(pattern, password))