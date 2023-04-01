from flask import Blueprint, request, jsonify, make_response
from .utils import add_result, all_results, new_report, delivery_reports
from . import db
from .sms import send_sms
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

            message = f"Hello {patient_name} your test results are available input 1 to confirm collection"
            send_sms("+254777765656", message)
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


# @main.route("/user-response", methods=['POST', 'GET'])
# def user_response():
#     if request.method == 'POST':
#         date = request.values.get("date", None)
#         from_user = request.values.get("from", None)
#         message_id = request.values.get("id", None)
#         text = request.values.get("text")
#         ui
