from __main__ import db

class ChatNames(db.Model):
    chat_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    chat_name = db.Column(db.String(100), nullable=False)
    template_id = db.Column(db.Integer, nullable=True)
    