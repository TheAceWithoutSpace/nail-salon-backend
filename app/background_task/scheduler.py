from apscheduler.schedulers.background import BackgroundScheduler
from app.database import get_db
from app.background_task.reminder import send_appointment_reminders


def schedule_reminder_job():
    scheduler = BackgroundScheduler()

    def job():
        db = next(get_db())  # Manually get DB session
        try:
            send_appointment_reminders(db)
        finally:
            db.close()

    scheduler.add_job(job, 'interval', hours=1)
    scheduler.start()