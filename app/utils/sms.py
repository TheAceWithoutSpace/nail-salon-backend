import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("INFOBIP_API_KEY")
BASE_URL = os.getenv("INFOBIP_BASE_URL")
SENDER = os.getenv("INFOBIP_SENDER")


def send_sms(phone_number: str, message: str) -> bool:
    url = f"{BASE_URL}/sms/2/text/advanced"
    headers = {
        "Authorization": f"App {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "messages": [
            {
                "from": SENDER,
                "destinations": [{"to": phone_number}],
                "text": message
            }
        ]
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.status_code == 200 and response.json().get("messages", [{}])[0].get("status", {}).get(
        "groupName") == "PENDING_ACCEPTED"
