from fastapi import FastAPI
from app.routers import appointments, users, auth, shifts, worker, service
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(appointments.router)
app.include_router(shifts.router)
app.include_router(worker.router)
app.include_router(service.router)
