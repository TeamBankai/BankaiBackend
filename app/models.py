from . import db

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(50))
    patient_phone = db.Column(db.String(10), unique=True)
    result_status = db.Column(db.Integer)
