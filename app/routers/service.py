from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/services", tags=["Services"])


# Create a new service
@router.post("/", response_model=schemas.ServiceOut)
def create_service(service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    return crud.create_service(db, service)


# Get all services
@router.get("/", response_model=List[schemas.ServiceOut])
def get_services(db: Session = Depends(get_db)):
    return crud.get_services(db)


# Get a service by ID
@router.get("/{service_id}", response_model=schemas.ServiceOut)
def get_service_by_id(service_id: int, db: Session = Depends(get_db)):
    service = crud.get_service_by_id(db, service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


# Update a service by ID
@router.put("/{service_id}", response_model=schemas.ServiceOut)
def update_service(service_id: int, service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    updated_service = crud.update_service(db, service_id, service)
    if updated_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return updated_service


# Delete a service by ID
@router.delete("/{service_id}", response_model=schemas.ServiceOut)
def delete_service(service_id: int, db: Session = Depends(get_db)):
    deleted_service = crud.delete_service(db, service_id)
    if deleted_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return deleted_service
