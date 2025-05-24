import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("INFOBIP_API_KEY")
BASE_URL = os.getenv("INFOBIP_BASE_URL")
SENDER = os.getenv("INFOBIP_SENDER")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")


def send_whatsapp_opt_code(to, code):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": 'otp2',
            "language": {
                "code": "en_us"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": code}
                    ]
                },
                {
                    "type": "button",
                    "sub_type": "url",
                    "index": "0",
                    "parameters": [
                        {"type": "text", "text": code}  # {{2}} in button URL
                    ]
                }
            ]
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    print("Status:", response.status_code)
    print("Response:", response.json())


def format_israeli_number(local_number: str) -> str:
    # Remove spaces, dashes, etc.
    digits = ''.join(filter(str.isdigit, local_number))

    # Remove leading zero if it exists
    if digits.startswith("0"):
        digits = digits[1:]

    # Add country code for Israel
    return f"+972{digits}"
