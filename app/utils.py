from . import db
from .models import Result, DeliveryReports


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
