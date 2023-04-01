import os
import requests
from urllib.parse import urlencode

username = "sandbox"
api_key = "47246e11613b9f71c704e8d8dea56ae4f2c2fae8382152572fc8c56c6f8426f5"

# africastalking.initialize(username, api_key)
# sms = africastalking.SMS


# def send_sms(phone: str, message: str):
#     def on_finish(error, response):
#         if error is not None:
#             raise error
#         print(response)

#     sms.send_premium(message,"72225", [phone], callback=on_finish)


def send_sms(phone: str, message: str):
    url = "https://api.sandbox.africastalking.com/version1/messaging"
    api_key = "47246e11613b9f71c704e8d8dea56ae4f2c2fae8382152572fc8c56c6f8426f5"

    data = urlencode({
        "username": "sandbox",
        "to": phone,
        "message": message,
        "from": os.environ.get('SHORT_CODE', '72225'),
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
    return True
