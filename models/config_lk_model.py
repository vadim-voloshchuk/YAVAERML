from __main__ import db

class ConfigLK(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    design = db.Column(db.String(10), nullable=False, default="basic blue")
    tariff_plan = db.Column(db.String(20), nullable=True)