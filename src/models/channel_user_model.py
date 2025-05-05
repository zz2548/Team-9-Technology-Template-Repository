"""
Channel-User join table model for the chat application.
This model represents the many-to-many relationship between users and channels.
"""
from datetime import datetime
from src.models import db


class ChannelUserModel(db.Model):
    """
    Model representing user membership in a channel.

    This is a join table for the many-to-many relationship between
    users and channels. It allows tracking which users have joined
    which channels, along with metadata like the join timestamp.
    """
    __tablename__ = "channel_users"

    # Primary key columns
    channel_id = db.Column(db.String(36), db.ForeignKey("channels.id"),
                           primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), primary_key=True)

    # Metadata columns
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        """String representation of the channel-user relationship."""
        return f"<ChannelUser channel_id={self.channel_id} user_id={self.user_id}>"