from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

# Association table for channel members
channel_members = db.Table('channel_members',
                           db.Column('user_id', db.Integer, db.ForeignKey('users.id'),
                                     primary_key=True),
                           db.Column('channel_id', db.Integer,
                                     db.ForeignKey('channels.id'), primary_key=True)
                           )


class User(UserMixin, db.Model):
    """User model for authentication and user profiles"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128))
    display_name = db.Column(db.String(64))
    avatar = db.Column(db.String(256))
    status = db.Column(db.String(20), default='offline')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    messages = db.relationship('Message', backref='author', lazy='dynamic')
    owned_channels = db.relationship('Channel', backref='owner', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'display_name': self.display_name or self.username,
            'avatar': self.avatar,
            'status': self.status,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None
        }

    def __repr__(self):
        return f'<User {self.username}>'


class Channel(db.Model):
    """Channel model for group conversations"""
    __tablename__ = 'channels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256))
    is_direct = db.Column(db.Boolean, default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    messages = db.relationship('Message', backref='channel', lazy='dynamic')
    members = db.relationship('User', secondary=channel_members,
                              backref=db.backref('channels', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_direct': self.is_direct,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat(),
            'member_count': len(self.members)
        }

    def __repr__(self):
        return f'<Channel {self.name}>'


class Message(db.Model):
    """Message model for user messages in channels"""
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'channel_id': self.channel_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'author': self.author.to_dict()
        }

    def __repr__(self):
        return f'<Message {self.id}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))