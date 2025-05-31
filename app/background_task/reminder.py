import os

import requests
from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.models import Appointment, AppointmentStatus

from sqlalchemy import cast, Date

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")


def send_whatsapp_reminder(to: str, customer_name: str, worker_name: str, appt_time: str, service: str, contact: str):
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
            "name": 'reminder',  # WhatsApp template name
            "language": {
                "code": "he"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": customer_name},  # {{1}}
                        {"type": "text", "text": worker_name},  # {{2}}
                        {"type": "text", "text": appt_time},  # {{3}}
                        {"type": "text", "text": service},  # {{4}}
                        {"type": "text", "text": contact},  # {{5}}
                    ]
                }
            ]
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    print(f"[Reminder] Sent to {to}: {response.status_code} {response.json()}")


def send_appointment_reminders(db: Session):
    today = date.today()
    tomorrow = today + timedelta(days=1)

    appointments = db.query(Appointment).filter(
        Appointment.reminder_sent == False,
        Appointment.status == AppointmentStatus.BOOKED,
        cast(Appointment.appointment_time, Date).in_([today, tomorrow])
    ).all()

    for appt in appointments:
        if not appt.user or not appt.worker:
            continue

        time_str = appt.appointment_time.strftime("%d/%m/%Y %H:%M")

        send_whatsapp_reminder(
            to=appt.user.phone_number,
            customer_name=appt.user.first_name + " " + appt.user.last_name,
            worker_name=appt.worker.first_name + " " + appt.worker.last_name,
            appt_time=time_str,
            service=appt.service,
            contact=appt.worker.phone_number
        )

        appt.reminder_sent = True

    db.commit()
