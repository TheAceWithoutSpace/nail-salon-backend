from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
from app.models.user import User
from app.models.verufy_code import VerifyCode
from app.utils.sms import send_sms


# Send OTP code to user's phone
def send_login_code(phone_number: str, db: Session):
    code = str(random.randint(100000, 999999))
    expires = datetime.utcnow() + timedelta(minutes=5)

    # Remove any previous entries for the phone number
    db.query(VerifyCode).filter(VerifyCode.phone_number == phone_number).delete()

    # Create and save new OTP record
    db.add(VerifyCode(phone_number=phone_number, code=code, expires_at=expires))
    db.commit()

    # Send the OTP via SMS
    message = f"Your nail salon verification code is {code}"
    send_sms(phone_number, message)
    return {"message": "OTP sent"}


# Verify OTP code
def verify_login_code(phone_number: str, code: str, db: Session):
    entry = db.query(VerifyCode).filter(
        VerifyCode.phone_number == phone_number,
        VerifyCode.code == code,
        VerifyCode.expires_at > datetime.utcnow()
    ).first()

    if not entry:
        return None  # Invalid or expired code

    # If the code is valid, check if the user exists or create a new one
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if not user:
        user = User(phone_number=phone_number, first_name="", last_name="", birthday=datetime(2000, 1, 1),
                    is_verified=1)
        db.add(user)
        db.commit()
        db.refresh(user)

    return user
