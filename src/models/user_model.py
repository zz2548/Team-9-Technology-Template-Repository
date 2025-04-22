
from src.models import db


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
