"""
Authentication module for the chat application.
Provides functions for token generation, validation and user authentication.
"""

import jwt
import datetime
import os
from functools import wraps
from flask import request, jsonify, current_app
from src.models.user_model import UserModel
from src.models import db

# Secret key for JWT encoding/decoding - in production, store this in environment variables
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-should-be-stored-in-env-var')
# Token expiration time (in minutes)
TOKEN_EXPIRATION = int(os.getenv('TOKEN_EXPIRATION', '1440'))  # Default 24 hours


def generate_token(user_id):
    """
    Generate a JWT token for user authentication.

    Args:
        user_id (str): The ID of the user to generate a token for

    Returns:
        str: The generated JWT token
    """
    try:
        # Create the token payload
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(
                minutes=TOKEN_EXPIRATION),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }

        # Generate the token
        return jwt.encode(
            payload,
            JWT_SECRET,
            algorithm='HS256'
        )
    except Exception as e:
        return str(e)


def decode_token(token):
    """
    Decode and validate a JWT token.

    Args:
        token (str): The JWT token to decode

    Returns:
        dict: The decoded token payload, or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def token_required(f):
    """
    Decorator for routes that require token authentication.

    This decorator extracts and validates a JWT token from the Authorization header
    and makes the authenticated user available to the route function.

    Usage:
        @app.route('/protected')
        @token_required
        def protected(current_user):
            return jsonify({'message': f'Hello {current_user.username}'})
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        # Debug logging to see what's being received
        current_app.logger.info(f"Auth header: {auth_header}")

        if auth_header:
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            current_app.logger.warning("No token provided in request")
            return jsonify({'error': 'Authentication required'}), 401

        try:
            # Debug token decoding
            current_app.logger.info(f"Attempting to decode token: {token[:10]}...")
            payload = decode_token(token)

            if not payload:
                current_app.logger.warning("Invalid token payload")
                return jsonify({'error': 'Invalid token'}), 401

            user_id = payload.get('sub')
            if not user_id:
                current_app.logger.warning("No user_id in token payload")
                return jsonify({'error': 'Invalid token format'}), 401

            current_user = db.session.get(UserModel, user_id)

            if not current_user:
                current_app.logger.warning(f"User not found for ID: {user_id}")
                return jsonify({'error': 'User not found'}), 401

        except Exception as e:
            current_app.logger.error(f"Token validation error: {str(e)}")
            return jsonify({'error': 'Token validation failed'}), 401

        return f(current_user, *args, **kwargs)

    return decorated