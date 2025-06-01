from fastapi import FastAPI

from app.background_task.scheduler import schedule_reminder_job
from app.routers import appointments, users, auth, shifts, worker, service
from app.database import Base, engine

# Base.metadata.create_all(bind=engine)

app = FastAPI()
# Routes
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(appointments.router)
app.include_router(shifts.router)
app.include_router(worker.router)
app.include_router(service.router)


# Scheduler
@app.on_event("startup")
def startup_event():
    schedule_reminder_job()


def safe_create_db():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        # Log it — don't crash on ENUM already exists, etc.
        print(f"[WARNING] DB init failed: {e}")


safe_create_db()  # ✅ auto-run with safety
