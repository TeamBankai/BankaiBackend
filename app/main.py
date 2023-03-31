from flask import Blueprint, request


main = Blueprint('main', __name__)


@main.route('/')
def index():
  return "<p>Hello World</>"


@main.route('/tests', methods=['POST', 'GET'])
def tests():
  if request.method == 'GET':
    return "GET TESTS"
