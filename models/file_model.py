from __main__ import db

class File(db.Model):
    chat_id = db.Column(db.Integer, primary_key=True)
    message_number = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(100), nullable=False)
    file = db.Column(db.dialects.mysql.MEDIUMBLOB, nullable=False)
