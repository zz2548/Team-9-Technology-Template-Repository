from flask_login import UserMixin
from src.models import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid


class UserModel(db.Model, UserMixin):
    """User model with Flask-Login compatibility."""
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    # Add relationships if using the ChannelUserModel
    channels = db.relationship(
        "ChannelModel",
        secondary="channel_users",
        back_populates="users"
    )

    def __init__(self, id=None, username=None, password=None):
        self.id = id or str(uuid.uuid4())
        self.username = username
        if password:
            self.set_password(password)

    def set_password(self, password):
        """Hash and store the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the provided password matches the stored hash."""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """Required by Flask-Login, returns the user's ID as a string."""
        return self.id

    def __repr__(self):
        return f"<User {self.username}>"