from src.models import db
from flask_sqlalchemy.model import Model as ModelType


class UserModel(db.Model, ModelType): # type: ignore[attr-defined]
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
