from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model 

from src.models import db

class ChannelModel(db.Model): # type: ignore[attr-defined]
    __tablename__ = 'channels'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
