import random
import uuid
from datetime import datetime, timedelta, date

import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from dotenv import load_dotenv
from app.models import Worker, Appointment, User
from app.schemas import UserCreate
from app.crud import user as crud_users

load_dotenv()

# Use a test-specific database URL (can be SQLite in-memory or separate test DB)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_TEST_URL", "sqlite:///:memory:")  # Default to in-memory SQLite
engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {})

# SessionLocal for the test environment
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency override to use the test database session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the default get_db dependency with the test database session
app.dependency_overrides[get_db] = override_get_db


# Test client fixture


# Fixture to create and drop the database for each test module
@pytest.fixture(scope="module")
def db_session():
    # Create the tables in the test database
    Base.metadata.create_all(bind=engine)

    # Create a session to interact with the database
    db = TestingSessionLocal()
    yield db

    # Drop the tables after the tests run
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client(db_session):
    with TestClient(app) as c:
        yield c


@pytest.fixture
def create_worker(db_session):
    def _create_worker(first_name="John", last_name="Doe", phone_number=None, email=None):
        if email is None:
            email = f"johndoe_{uuid.uuid4().hex[:6]}@example.com"
        if phone_number is None:
            phone_number = f"10000000{random.randint(100, 999)}"
        worker = Worker(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email
        )
        db_session.add(worker)
        db_session.commit()
        db_session.refresh(worker)
        return worker

    return _create_worker


@pytest.fixture
def create_user(db_session):
    def _create_user():
        email = f"johndoe_{uuid.uuid4().hex[:6]}@example.com"
        phone_number = f"10000000{random.randint(100, 999)}"

        user_data = UserCreate(
            phone_number=phone_number,
            first_name="John",
            last_name="Test",
            email=email,
            birthdate=date(1990, 1, 1)
        )
        user = User(
            phone_number=user_data.phone_number,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            birthdate=user_data.birthdate,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    return _create_user


# Appointment creation fixture for tests
@pytest.fixture
def create_appointment(db_session, create_user, create_worker):
    def _create_appointment(user=None, worker=None, appointment_time=None, service="Nail Service", user_request="None"):
        if user is None:
            user = create_user()
        if worker is None:
            worker = create_worker()
        if appointment_time is None:
            appointment_time = datetime.utcnow() + timedelta(days=1)  # Default to 1 day ahead

        appointment = Appointment(
            user_id=user.id,
            worker_id=worker.id,
            service=service,
            appointment_time=appointment_time,
            user_request=user_request
        )
        db_session.add(appointment)
        db_session.commit()
        db_session.refresh(appointment)
        return appointment

    return _create_appointment


# Optional: Cleanup database after tests (if needed)
@pytest.fixture(scope="module", autouse=True)
def cleanup_database(db_session):
    yield
    # Clean up database after tests if needed
    try:
        db_session.query(Appointment).delete()
    except Exception as e:
        print(f"Skipping Appointment cleanup: {e}")
    try:
        db_session.query(Worker).delete()
    except Exception as e:
        print(f"Skipping Worker cleanup: {e}")

    try:
        db_session.query(User).delete()
    except Exception as e:
        print(f"Skipping User cleanup: {e}")

    db_session.commit()
