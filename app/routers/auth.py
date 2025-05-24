from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.utils.jwt_auth import create_jwt_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/send-login-code")
def send_login_code(request: schemas.SendLoginCodeRequest, db: Session = Depends(get_db)):
    return crud.send_login_code(request.phone_number, db)


@router.post("/verify-login-code")
def verify_login_code(request: schemas.VerifyLoginCodeRequest, db: Session = Depends(get_db)):
    user = crud.verify_login_code(request.phone_number, request.code, db)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired code")

    # Create JWT token for the authenticated user
    token = create_jwt_token(user)
    return {"access_token": token, "token_type": "bearer"}
