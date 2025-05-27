from sqlalchemy.orm import Session
from app import models, schemas


# Create a new service
def create_service(db: Session, service: schemas.ServiceCreate):
    db_service = models.Service(
        name=service.name,
        price=service.price,
        duration=service.duration,
        description=service.duration
    )
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


# Get all services
def get_services(db: Session):
    return db.query(models.Service).all()


# Get a service by its ID
def get_service_by_id(db: Session, service_id: int):
    return db.query(models.Service).filter(models.Service.id == service_id).first()


# Update a service
def update_service(db: Session, service_id: int, service: schemas.ServiceCreate):
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if db_service:
        db_service.name = service.name
        db_service.price = service.price
        db_service.duration = service.duration
        db_service.description = service.description
        db.commit()
        db.refresh(db_service)
        return db_service
    return None


# Delete a service
def delete_service(db: Session, service_id: int):
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if db_service:
        db.delete(db_service)
        db.commit()
        return db_service
    return None
