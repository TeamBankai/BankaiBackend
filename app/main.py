from flask import Blueprint, request, jsonify, make_response, redirect, url_for
from .utils import add_result, all_results, new_report, delivery_reports, new_patient, update_patient, find_patient, all_patients
from . import db
from .sms import send_sms
from datetime import datetime
from .models import Patient
import requests
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
            new_patient(patient_phone)

            message = f"Hello {patient_name} your test results are available reply with 'CONFIRM' to confirm collection\nReply with 'STOP' to opt out"
            send_sms(phone_number, message)
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
                'phone': result.patient_phone
            })
        return jsonify(serialized)


@main.route("/delivery-reports", methods=['POST', 'GET', 'PUT'])
def new_delivery_report():
    if request.method == "POST":
        status = request.values.get("status", None)
        network_code = request.values.get("networkCode", None)
        phone_number = request.values.get("phoneNumber", None)
        failure_reason = request.values.get("failureReason")

        # if find_patient(phone_number):
        #     update_patient(phone_number,
        #                    first_msg_time=datetime.now(), subscription_status="1")
        phone = "0" + phone_number[4:]
        url = f"http://localhost:5000/update-delivery-time/{phone}"

        payload = {}
        headers = {}

        response = requests.request(
            "PUT", url, headers=headers, data=payload)
        print(response.text)

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


@main.route("/user-response", methods=['POST', 'GET', 'PUT'])
def user_response():
    if request.method == 'POST':
        date = request.values.get("date")
        from_user = request.values.get("from")
        message_id = request.values.get("id", None)
        text = request.values.get("text").strip()
        link_id = request.values.get("linkId", None)

        data = {
            "date": date,
            "from_user": from_user,
            "message_id": message_id,
            "text": text,
            "link_id": link_id
        }

        if text == "CONFIRM":
            # patient = find_patient(from_user)
            # if patient:
            #     if patient.appointment_status != "confirmed":
            #         datetime_object = datetime.strptime(
            #             date, '%Y-%m-%d %H:%M:%S')
            #         # update_patient(
            #         #     from_user, first_res_time=datetime_object, appointment_status="confirmed")
            # send_sms(
            #     from_user, "Please collect your results from facilityName within the next 3 days\nreply with 'STOP' to stop opt out")
            # calling update-appointments route
            phone_number = "0" + from_user[4:]
            url = f"http://localhost:5000/update-appointments/{phone_number}"

            payload = {}
            headers = {}

            response = requests.request(
                "PUT", url, headers=headers, data=payload)
            print(response.text)
            # requests.put(url_for('main.update_appointments',  phone={phone_number}))
            # return redirect(url_for('main.update_appointments', phone=from_user))
            #     else:
            #         pass
            # else:
            #     pass
        elif text == "STOP":
            if find_patient(from_user):
                update_patient(subscription_status="0")
                send_sms(from_user, "You have been successfully unsubscribed")
            else:
                pass

    return jsonify(data)

    # if request.method == 'GET':
    #     pass


@main.route("/update-appointments/<phone>", methods=['PUT'])
def update_appointments(phone):
    patient = Patient.query.filter_by(phone=phone).first_or_404()
    patient.appointment_status = "confirmed"
    patient.first_res_time = datetime.now()
    db.session.commit()

    send_sms(phone, "Please collect your results from facilityName within the next 3 days\nreply with 'STOP' to stop receiving updates")

    return jsonify({"message": "appointment updated successfully"})


@main.route("/update-delivery-time/<phone>", methods=['PUT'])
def update_delivery_time(phone):
    patient = Patient.query.filter_by(phone=phone).first_or_404()
    patient.first_msg_time = datetime.now()
    db.session.commit()

    return jsonify({"message": "delivery time updated"})


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
        turnaround_time = (patient.first_res_time -
                           patient.first_msg_time).total_seconds()

        hours = int(turnaround_time / 3600)
        minutes = int((turnaround_time % 3600) / 60)
        seconds = int(turnaround_time % 60)
        serialized.append({
            'id': patient.id,
            'phone': patient.phone,
            'delivered_time': patient.first_msg_time,
            'response_time': patient.first_res_time,
            'subscription': patient.subscription_status,
            'result_deadline': patient.latest_slot,
            'tat': f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        })
    return jsonify(serialized)


# 'tat': f"{hours:02d}:{minutes:02d}:{seconds:02d}"
