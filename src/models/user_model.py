from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model 

from src.models import db

class UserModel(Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
