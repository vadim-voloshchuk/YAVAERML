from __main__ import db

class Template(db.Model):
    template_id = db.Column(db.Integer, primary_key=True)
    template_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    template_file = db.Column(db.dialects.mysql.MEDIUMBLOB, nullable=False)