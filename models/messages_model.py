from __main__ import db

class Messages(db.Model):
    message_number = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    have_file = db.Column(db.Boolean, nullable=False)
    is_user = db.Column(db.Boolean, nullable=False)
