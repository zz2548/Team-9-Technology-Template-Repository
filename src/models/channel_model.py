from src.models import db
from flask_sqlalchemy.model import Model as ModelType

class ChannelModel(db.Model, ModelType): # type: ignore[attr-defined]
    __tablename__ = 'channels'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
