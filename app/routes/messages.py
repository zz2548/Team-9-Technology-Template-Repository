from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from flask_socketio import emit
from app import db, socketio
from app.models import Message, Channel
from datetime import datetime

messages = Blueprint('messages', __name__)


@messages.route('/api/channels/<int:channel_id>/messages', methods=['GET'])
@login_required
def get_messages(channel_id):
    """API endpoint to get messages from a channel"""
    channel = Channel.query.get_or_404(channel_id)

    # Check if user is a member of the channel
    if current_user not in channel.members:
        return jsonify({'error': 'You are not a member of this channel'}), 403

    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    # Get messages with pagination (newest first)
    messages_query = Message.query.filter_by(channel_id=channel_id) \
        .order_by(Message.created_at.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    messages_list = [message.to_dict() for message in messages_query.items]

    return jsonify({
        'messages': messages_list,
        'total': messages_query.total,
        'pages': messages_query.pages,
        'page': page
    })


@messages.route('/api/channels/<int:channel_id>/messages', methods=['POST'])
@login_required
def create_message(channel_id):
    """API endpoint to create a new message in a channel"""
    channel = Channel.query.get_or_404(channel_id)

    # Check if user is a member of the channel
    if current_user not in channel.members:
        return jsonify({'error': 'You are not a member of this channel'}), 403

    data = request.get_json()
    content = data.get('content')

    if not content or not content.strip():
        return jsonify({'error': 'Message content is required'}), 400

    # Create new message
    message = Message(
        content=content,
        user_id=current_user.id,
        channel_id=channel_id
    )

    db.session.add(message)
    db.session.commit()

    # Convert to dict for JSON response
    message_dict = message.to_dict()

    # Emit a socket event to notify clients of new message
    socketio.emit('new_message', message_dict, room=f'channel_{channel_id}')

    return jsonify({
        'message': 'Message sent successfully',
        'data': message_dict
    }), 201


@messages.route('/api/messages/<int:message_id>', methods=['PUT'])
@login_required
def update_message(message_id):
    """API endpoint to update a message"""
    message = Message.query.get_or_404(message_id)

    # Check if user is the author of the message
    if message.user_id != current_user.id:
        return jsonify({'error': 'You can only edit your own messages'}), 403

    data = request.get_json()
    content = data.get('content')

    if not content or not content.strip():
        return jsonify({'error': 'Message content is required'}), 400

    message.content = content
    message.updated_at = datetime.utcnow()
    db.session.commit()

    # Convert to dict for JSON response
    message_dict = message.to_dict()

    # Emit a socket event to notify clients of message update
    socketio.emit('update_message', message_dict, room=f'channel_{message.channel_id}')

    return jsonify({
        'message': 'Message updated successfully',
        'data': message_dict
    })


@messages.route('/api/messages/<int:message_id>', methods=['DELETE'])
@login_required
def delete_message(message_id):
    """API endpoint to delete a message"""
    message = Message.query.get_or_404(message_id)

    # Check if user is the author of the message or channel owner
    channel = Channel.query.get(message.channel_id)
    if message.user_id != current_user.id and channel.owner_id != current_user.id:
        return jsonify({'error': 'You cannot delete this message'}), 403

    channel_id = message.channel_id

    db.session.delete(message)