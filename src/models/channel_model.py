from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

Base = db.Model 

class ChannelModel(Base): # type: ignore[attr-defined]
    __tablename__ = 'channels'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
