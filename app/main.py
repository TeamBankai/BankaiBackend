from flask import Blueprint, request, jsonify, make_response
from .utils import add_result, all_results, new_report, delivery_reports, new_patient, update_patient, find_patient, all_patients
from . import db
from .sms import send_sms
from datetime import datetime
import re


main = Blueprint('main', __name__)


@main.route('/tests', methods=['POST', 'GET'])
def tests():
    if request.method == "POST":
        data = request.json
        required_fields = ['patient_name', 'patient_phone']

        if all(field in data for field in required_fields):
            patient_name = data.get('patient_name')
            patient_phone = data.get('patient_phone')
            # Validate result params
            if not re.match("^\w+$", patient_name):
                return "Invalid value on name parameter", 400
            if not re.match("^(07|01)\d{8}$", patient_phone):
                return "Invalid phone number", 400

            add_result(patient_phone, patient_name)
            phone_number = "+254" + patient_phone[1:]
            new_patient(phone_number)

            message = f"Hello {patient_name} your test results are available reply with 'CONFIRM' to confirm collection"
            send_sms("+254777287562", message)
            return "Data successfully stored in database", 201
        else:
            # Required fields are missing, return an error response
            return "Missing required fields: {}".format(", ".join(set(required_fields) - set(data))), 400

    if request.method == "GET":
        results = all_results()

        serialized = []
        for result in results:
            serialized.append({
                'id': result.id,
                'name': result.patient_name,
                'description': result.patient_phone
            })
        return jsonify(serialized)


@main.route("/delivery-reports", methods=['POST', 'GET'])
def new_delivery_report():
    if request.method == "POST":
        status = request.values.get("status", None)
        network_code = request.values.get("networkCode", None)
        phone_number = request.values.get("phoneNumber", None)
        failure_reason = request.values.get("failureReason")

        patient_phone_number = "+254" + phone_number[1:]
        if find_patient(patient_phone_number):
            update_patient(patient_phone_number,
                        first_msg_time=datetime.now(), subscription_status="OK")

        data = {
            "status": status,
            "network_code": network_code,
            "phone_number": phone_number,
            "failure_reason": failure_reason
        }

        new_report(status, network_code, failure_reason, phone_number)

        return jsonify(data)

    if request.method == 'GET':
        reports = delivery_reports()

        serialized = []
        for report in reports:
            serialized.append({
                'id': report.id,
                'time': report.time,
                'status': report.status,
                'network_code': report.network_code,
                'failure_reason': report.failure_reason,
                'phone_number': report.phone_number
            })
        return jsonify(serialized)


@main.route("/user-response", methods=['POST', 'GET'])
def user_response():
    if request.method == 'POST':
        date = request.values.get("date")
        from_user = request.values.get("from")
        message_id = request.values.get("id", None)
        text = request.values.get("text")
        link_id = request.values.get("linkId", None)

        if text == "CONFIRM":
            send_sms(
                from_user, "Appointment confirmed\nText STOP to stop receiving updates")

        data = {
            "date": date,
            "from_user": from_user,
            "message_id": message_id,
            "text": text,
            "link_id": link_id
        }

    return jsonify(data)


@main.route("/opt-outs", methods=['POST', 'GET'])
def opt_outs():
    if request.method == 'POST':
        from_user = request.values.get("phoneNumber")

        return from_user


@main.route("/patients-data")
def patient_data():
    results = all_patients()

    serialized = []
    for patient in results:
            serialized.append({
                'id': patient.id,
                'phone': patient.phone,
                # 'description': patient.
            })
    return jsonify(serialized)
