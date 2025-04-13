from src.models import db
from flask_sqlalchemy.model import Model as ModelType

class MessageModel(db.Model, ModelType):  # type: ignore[attr-defined]
    __tablename__ = 'messages'
    id = db.Column(db.String, primary_key=True)
    sender_id = db.Column(db.String, db.ForeignKey('users.id'))
    channel_id = db.Column(db.String, db.ForeignKey('channels.id'))
    content = db.Column(db.Text, nullable=False)
