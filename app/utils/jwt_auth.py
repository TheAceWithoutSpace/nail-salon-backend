from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        print(user_id)
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def create_jwt_token(user):
    token = jwt.encode({"user_id": user.id, "exp": datetime.utcnow() + timedelta(hours=24)},
                       SECRET_KEY, algorithm=ALGORITHM)
    return token
