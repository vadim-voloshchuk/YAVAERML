from __main__ import db

class Description(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(10000))
