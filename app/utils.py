from . import db
from .models import Result, DeliveryReports, Patient


def add_result(phone: str, name: str):
    new_result = Result(patient_name=name,
                        patient_phone=phone, result_status=0)
    db.session.add(new_result)
    db.session.commit()


def all_results():
    return Result.query.all()


def new_report(status, network_code, failure_reason, phone_number):
    new_report = DeliveryReports(status=status, network_code=network_code,
                                 failure_reason=failure_reason, phone_number=phone_number)
    db.session.add(new_report)
    db.session.commit()


def delivery_reports():
    return DeliveryReports.query.all()


def new_patient(phone: str):
    new_patient = Patient(phone=phone)
    db.session.add(new_patient)
    db.session.commit()


def all_patients():
    return Patient.query.all()


def find_patient(phone_number):
    return Patient.query.filter_by(phone=phone_number).first()


def update_patient(phone, *args, **kwargs):
    patient = Patient.query.filter_by(phone=phone).first_or_404()
    if patient:
        for key, value in kwargs.items():
            (patient, key, value)
        db.session.commit()
