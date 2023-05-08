from __main__ import db

class Template(db.Model):
    template_name = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    template_file = db.Column(db.dialects.mysql.MEDIUMBLOB)