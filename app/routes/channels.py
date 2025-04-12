from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Channel, User

channels = Blueprint('channels', __name__)


@channels.route('/')
@login_required
def index():
    """Display the main channels page"""
    user_channels = current_user.channels.all()
    return render_template('channels.html', channels=user_channels)


@channels.route('/api/channels', methods=['GET'])
@login_required
def get_channels():
    """API endpoint to get a list of channels the user is a member of"""
    user_channels = current_user.channels.all()
    return jsonify({
        'channels': [channel.to_dict() for channel in user_channels]
    })


@channels.route('/api/channels', methods=['POST'])
@login_required
def create_channel():
    """API endpoint to create a new channel"""
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    is_direct = data.get('is_direct', False)
    member_ids = data.get('member_ids', [])

    if not name:
        return jsonify({'error': 'Channel name is required'}), 400

    # Create new channel
    channel = Channel(
        name=name,
        description=description,
        is_direct=is_direct,
        owner_id=current_user.id
    )

    # Add current user to members
    channel.members.append(current_user)

    # Add other members if provided
    if member_ids:
        for member_id in member_ids:
            user = User.query.get(member_id)
            if user and user.id != current_user.id:
                channel.members.append(user)

    db.session.add(channel)
    db.session.commit()

    return jsonify({
        'message': 'Channel created successfully',
        'channel': channel.to_dict()
    }), 201


@channels.route('/api/channels/<int:channel_id>', methods=['GET'])
@login_required
def get_channel(channel_id):
    """API endpoint to get a specific channel"""
    channel = Channel.query.get_or_404(channel_id)

    # Check if user is a member of the channel
    if current_user not in channel.members:
        return jsonify({'error': 'You are not a member of this channel'}), 403

    return jsonify({
        'channel': channel.to_dict(),
        'members': [member.to_dict() for member in channel.members]
    })


@channels.route('/api/channels/<int:channel_id>', methods=['PUT'])
@login_required
def update_channel(channel_id):
    """API endpoint to update a channel"""
    channel = Channel.query.get_or_404(channel_id)

    # Check if user is the owner of the channel
    if channel.owner_id != current_user.id:
        return jsonify({'error': 'Only the channel owner can update the channel'}), 403

    data = request.get_json()

    if 'name' in data:
        channel.name = data['name']
    if 'description' in data:
        channel.description = data['description']

    db.session.commit()

    return jsonify({
        'message': 'Channel updated successfully',
        'channel': channel.to_dict()
    })


@channels.route('/api/channels/<int:channel_id>', methods=['DELETE'])
@login_required
def delete_channel(channel_id):
    """API endpoint to delete a channel"""
    channel = Channel.query.get_or_404(channel_id)

    # Check if user is the owner of the channel
    if channel.owner_id != current_user.id:
        return jsonify({'error': 'Only the channel owner can delete the channel'}), 403

    db.session.delete(channel)
    db.session.commit()

    return jsonify({
        'message': 'Channel deleted successfully'
    })


@channels.route('/api/channels/<int:channel_id>/members', methods=['POST'])
@login_required
def add_member(channel_id):
    """API endpoint to add a member to a channel"""
    channel = Channel.query.get_or_404(channel_id)

    # Check if user is a member of the channel
    if current_user not in channel.members:
        return jsonify({'error': 'You are not a member of this channel'}), 403

    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    user = User.query.get_or_404(user_id)

    # Check if user is already a member
    if user in channel.members:
        return jsonify({'error': 'User is already a member of this channel'}), 400

    channel.members.append(user)
    db.session.commit()

    return jsonify({
        'message': 'Member added successfully'
    })


@channels.route('/api/channels/<int:channel_id>/members/<int:user_id>',
                methods=['DELETE'])
@login_required
def remove_member(channel_id, user_id):
    """API endpoint to remove a member from a channel"""
    channel = Channel.query.get_or_404(channel_id)

    # Only the channel owner or the member themselves can remove a member
    if channel.owner_id != current_user.id and user_id != current_user.id:
        return jsonify(
            {'error': 'You do not have permission to remove this member'}), 403

    user = User.query.get_or_404(user_id)

    # Check if user is a member
    if user not in channel.members:
        return jsonify({'error': 'User is not a member of this channel'}), 400

    # Cannot remove the owner from their own channel
    if user.id == channel.owner_id:
        return jsonify({'error': 'Cannot remove the channel owner'}), 400

    channel.members.remove(user)
    db.session.commit()

    return jsonify({
        'message': 'Member removed successfully'
    })


@channels.route('/channels/<int:channel_id>')
@login_required
def view_channel(channel_id):
    """Display the channel view page"""
    channel = Channel.query.get_or_404(channel_id)

    # Check if user is a member of the channel
    if current_user not in channel.members:
        flash('You are not a member of this channel')
        return redirect(url_for('channels.index'))

    return render_template('chat.html', channel=channel)