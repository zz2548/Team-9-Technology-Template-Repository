from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from app import db
from app.models import User

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user"""
    if current_user.is_authenticated:
        return redirect(url_for('channels.index'))

    if request.method == 'POST':
        # Handle API requests
        if request.headers.get('Content-Type') == 'application/json':
            data = request.get_json()
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            # Check if user already exists
            if User.query.filter_by(username=username).first():
                return jsonify({'error': 'Username already exists'}), 400
            if User.query.filter_by(email=email).first():
                return jsonify({'error': 'Email already exists'}), 400

            # Create new user
            new_user = User(
                username=username,
                email=email,
                password=password  # This will use the password setter method
            )
            db.session.add(new_user)
            db.session.commit()

            return jsonify({'message': 'User registered successfully'}), 201

        # Handle form submissions
        else:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

            # Check if user already exists
            if User.query.filter_by(username=username).first():
                flash('Username already exists')
                return redirect(url_for('auth.register'))
            if User.query.filter_by(email=email).first():
                flash('Email already exists')
                return redirect(url_for('auth.register'))

            # Create new user
            new_user = User(
                username=username,
                email=email,
                password=password  # This will use the password setter method
            )
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! Please log in.')
            return redirect(url_for('auth.login'))

    # GET request - show registration form
    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Log in a user"""
    if current_user.is_authenticated:
        return redirect(url_for('channels.index'))

    if request.method == 'POST':
        # Handle API requests
        if request.headers.get('Content-Type') == 'application/json':
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            user = User.query.filter_by(username=username).first()

            # Check if user exists and password is correct
            if not user or not user.verify_password(password):
                return jsonify({'error': 'Invalid username or password'}), 401

            # Update user status and last seen
            user.status = 'online'
            user.last_seen = datetime.utcnow()
            db.session.commit()

            # Log in the user
            login_user(user)

            return jsonify({
                'message': 'Login successful',
                'user': user.to_dict()
            }), 200

        # Handle form submissions
        else:
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter_by(username=username).first()

            # Check if user exists and password is correct
            if not user or not user.verify_password(password):
                flash('Invalid username or password')
                return redirect(url_for('auth.login'))

            # Update user status and last seen
            user.status = 'online'
            user.last_seen = datetime.utcnow()
            db.session.commit()

            # Log in the user
            login_user(user)

            return redirect(url_for('channels.index'))

    # GET request - show login form
    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    """Log out a user"""
    # Update user status
    current_user.status = 'offline'
    current_user.last_seen = datetime.utcnow()
    db.session.commit()

    # Log out the user
    logout_user()

    # Handle API requests
    if request.headers.get('Accept') == 'application/json':
        return jsonify({'message': 'Logout successful'}), 200

    # Handle normal requests
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))