from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

Base = db.Model

class UserModel(Base): # type: ignore[attr-defined]
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
