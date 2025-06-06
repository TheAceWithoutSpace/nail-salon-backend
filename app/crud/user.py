from typing import List, Type

from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserUpdate, UserOut
from app.utils.message_sender import format_israeli_number


def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()


# Create a new user
def create_user(user: UserCreate, db: Session) -> User:
    phone_number = format_israeli_number(user.phone_number)
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=phone_number,
        email=user.email,
        birthdate=user.birthdate,
        user_type=user.user_type
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Get user by ID
def get_user_by_id(user_id: int, db: Session):
    return db.query(User).filter(User.id == user_id).first()


# Get user by phone number
def get_user_by_phone_number(phone_number: str, db: Session):
    return db.query(User).filter(User.phone_number == format_israeli_number(phone_number)).first()


# Get users by type
def get_users_by_type(user_type: str, db: Session) -> list[User]:
    return db.query(User).filter(User.user_type == user_type).all()


# Update user
def update_user(user_id: int, user: UserUpdate, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


# Delete user
def delete_user(user_id: int, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return {"message": "User deleted"}
    return {"message": "User not found"}


# Update user type
def update_user_type(user_id: int, new_type: str, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.user_type = new_type
        db.commit()
        db.refresh(db_user)
        return db_user
    return None
