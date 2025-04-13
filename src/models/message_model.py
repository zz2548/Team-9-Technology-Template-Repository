from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

Base = db.Model 

class MessageModel(Base):  # type: ignore[attr-defined]
    __tablename__ = 'messages'
    id = db.Column(db.String, primary_key=True)
    sender_id = db.Column(db.String, db.ForeignKey('users.id'))
    channel_id = db.Column(db.String, db.ForeignKey('channels.id'))
    content = db.Column(db.Text, nullable=False)
