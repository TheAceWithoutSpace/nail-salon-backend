from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserUpdate


# Create a new user
def create_user(user: UserCreate, db: Session) -> User:
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
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
    return db.query(User).filter(User.phone_number == phone_number).first()


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
