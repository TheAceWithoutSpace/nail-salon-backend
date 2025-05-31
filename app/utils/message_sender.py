import os
import requests
from dotenv import load_dotenv

load_dotenv()

# API_KEY = os.getenv("INFOBIP_API_KEY")
# BASE_URL = os.getenv("INFOBIP_BASE_URL")
# SENDER = os.getenv("INFOBIP_SENDER")
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
            "name": 'otp',
            "language": {
                "code": "He"
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
    # Remove non-digit characters, but preserve '+' if it starts the string
    local_number = local_number.strip().replace(" ", "").replace("-", "")

    if local_number.startswith("+972"):
        return local_number
    elif local_number.startswith("972"):
        return f"+{local_number}"
    elif local_number.startswith("0"):
        return f"+972{local_number[1:]}"
    else:
        # If it's already in correct format (or malformed), just add prefix
        return f"+972{local_number}"
