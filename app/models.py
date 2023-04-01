from . import db
from sqlalchemy.sql import func

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(50))
    patient_phone = db.Column(db.String(10))
    result_status = db.Column(db.Integer)


class DeliveryReports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime,  default=func.now())
    status = db.Column(db.String(20))
    network_code = db.Column(db.String(10))
    failure_reason = db.Column(db.String(50))
    phone_number = db.Column(db.String(20))

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(15), unique=True)
    first_msg_time = db.Column(db.DateTime)
    first_res_time = db.Column(db.DateTime)
    appointment_status = db.Column(db.String(10))
    subscription_status = db.Column(db.String(10))
    latest_slot = db.Column(db.DateTime)
