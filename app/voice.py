import os
from urllib.parse import urlencode
import requests
from dotenv import load_dotenv
import os


load_dotenv()

username = "sandbox"
api_key = os.environ.get('API_KEY_LIVE', None)
url = "https://voice.africastalking.com/call"


def initiate_call(from_phone: str, to_phone: str):
    data = urlencode({
        "username": os.environ.get('USERNAME', None),
        "to": to_phone,
        "from": from_phone
    })

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "apiKey": os.getenv('API_KEY_LIVE'),
    }

    res = requests.post(url, data=data, headers=headers)
    if res.status_code != 200:
        print(f"Error placing call: {res.text}")
        return False

    print(f"Call placed {res.text}")

    return True
