import os
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv
import os


load_dotenv()

username = "sandbox"
api_key = os.environ.get('API_KEY', None)
url = "https://api.sandbox.africastalking.com/version1/messaging"


def send_sms(phone: str, message: str):
    data = urlencode({
        "username": "sandbox",
        "to": phone,
        "message": message,
        "from": '7633'
    })

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "apikey": api_key,
    }

    res = requests.post(url, data=data, headers=headers)
    if res.status_code != 201:
        print(f"Error sending SMS: {res.text}")
        return False

    print("SMS sent successfully")
    print(res.text)
    return True
