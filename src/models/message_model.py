from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model 

from src.models import db

class MessageModel(db.Model):  
    __tablename__ = 'messages'
    id = db.Column(db.String, primary_key=True)
    sender_id = db.Column(db.String, db.ForeignKey('users.id'))
    channel_id = db.Column(db.String, db.ForeignKey('channels.id'))
    content = db.Column(db.Text, nullable=False)
