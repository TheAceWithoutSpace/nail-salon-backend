from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.models.user import UserType
from app.utils.jwt_auth import require_user_type

router = APIRouter(prefix="/users", tags=["Users"])


# Create a new user
@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    crud.send_login_code(user.phone_number, db)
    response = crud.create_user(user, db)
    print(response.user_type)
    return response


# get All Users
@router.get("/", response_model=list[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db), user=Depends(require_user_type("admin"))):
    return crud.get_all_users(db)


# Get a user by ID
@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(user_id, db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Get a user by phone number
@router.get("/phone/{phone_number}", response_model=schemas.UserOut)
def get_user_by_phone(phone_number: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_phone_number(phone_number, db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Update a user
@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(user_id, user, db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Delete a user
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(user_id, db)


# get users by type (worker, customer ,admin)
@router.get("/type/{user_type}", response_model=list[schemas.UserOut])
def get_users_by_type(user_type: UserType, db: Session = Depends(get_db)):
    return crud.get_users_by_type(user_type, db)


# change the user Type (worker)
@router.put("/type/worker", response_model=schemas.UserOut)
def update_user_type_to_worker(data: schemas.PromoteUserToWorker, db: Session = Depends(get_db),
                               user=Depends(require_user_type("admin"))):
    return crud.update_user_type(data.user_id, data.new_type, db)


# change the user Type (customer)
@router.put("/type/customer", response_model=schemas.UserOut)
def update_user_type_to_worker(data: schemas.PromoteUserToCustomer, db: Session = Depends(get_db),
                               user=Depends(require_user_type("admin"))):
    return crud.update_user_type(data.user_id, data.new_type, db)


# change the user Type (admin)
@router.put("/type/admin", response_model=schemas.UserOut)
def update_user_type_to_worker(data: schemas.PromoteUserToAdmin, db: Session = Depends(get_db),
                               user=Depends(require_user_type("admin"))):
    return crud.update_user_type(data.user_id, data.new_type, db)
