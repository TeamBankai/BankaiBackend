from flask import Blueprint, request, jsonify
import re


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return "<p>Hello World</>"


@main.route('/tests', methods=['POST'])
def tests():
    data = request.json
    required_fields = ['username', 'phone_number']

    if all(field in data for field in required_fields):
        username = data.get('username')
        phone_number = data.get('phone_number')
        # Validate result params
        if not re.match("^\w+$", username):
            return "Invalid username", 400
        if not re.match("^(07|01)\d{8}$", phone_number):
            return "Invalid phone number", 400
        # TODO: Implement data persistency to db
        return "Data successfully stored in database", 201
    else:
        # Required fields are missing, return an error response
        return "Missing required fields: {}".format(", ".join(set(required_fields) - set(data))), 400
