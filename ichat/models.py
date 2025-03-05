from datetime import datetime
from ichat import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_bot = db.Column(db.Boolean, default=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    send_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.String(150), nullable=False)

    def __str__(self):
        return f'Message from {self.sender_id} to {self.receiver_id} at {self.send_time}: {self.content}'