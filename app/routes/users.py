from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User

users = Blueprint('users', __name__)


@users.route('/api/users/me', methods=['GET'])
@login_required
def get_current_user():
    """Get the current logged-in user"""
    return jsonify({
        'user': current_user.to_dict()
    })


@users.route('/api/users/search', methods=['GET'])
@login_required
def search_users():
    """Search for users by username or display name"""
    query = request.args.get('q', '').strip()

    if not query or len(query) < 2:
        return jsonify({'users': []})

    # Search for users by username or display name
    users = User.query.filter(
        (User.username.ilike(f'%{query}%')) |
        (User.display_name.ilike(f'%{query}%'))
    ).limit(10).all()

    # Don't include the current user in results
    users = [user for user in users if user.id != current_user.id]

    return jsonify({
        'users': [user.to_dict() for user in users]
    })


@users.route('/api/users/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    """Get a specific user"""
    user = User.query.get_or_404(user_id)

    return jsonify({
        'user': user.to_dict()
    })


@users.route('/api/users/status', methods=['PUT'])
@login_required
def update_status():
    """Update the current user's status"""
    data = request.get_json()
    status = data.get('status')

    valid_statuses = ['online', 'idle', 'do_not_disturb', 'invisible', 'offline']

    if not status or status not in valid_statuses:
        return jsonify({'error': 'Invalid status'}), 400

    current_user.status = status
    db.session.commit()

    return jsonify({
        'message': 'Status updated successfully',
        'user': current_user.to_dict()
    })


@users.route('/api/users/me', methods=['PUT'])
@login_required
def update_profile():
    """Update the current user's profile"""
    data = request.get_json()

    if 'display_name' in data:
        current_user.display_name = data['display_name']

    if 'avatar' in data:
        current_user.avatar = data['avatar']

    db.session.commit()

    return jsonify({
        'message': 'Profile updated successfully',
        'user': current_user.to_dict()
    })