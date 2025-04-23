
from src.models import db


class ChannelModel(db.Model):
    __tablename__ = "channels"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
