from sqlalchemy.orm import Session
from app.models.worker import Worker
from app.schemas.worker import WorkerCreate, WorkerUpdate


# Create a new worker
def create_worker(db: Session, worker: WorkerCreate):
    db_worker = Worker(**worker.model_dump())
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker


# Get a worker by id
def get_worker(db: Session, worker_id: int):
    return db.query(Worker).filter(Worker.id == worker_id).first()


# Get all workers
def get_workers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Worker).offset(skip).limit(limit).all()


# Update a worker
def update_worker(db: Session, worker_id: int, worker: WorkerUpdate):
    db_worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if db_worker:
        for key, value in worker.model_dump(exclude_unset=True).items():
            setattr(db_worker, key, value)
        db.commit()
        db.refresh(db_worker)
        return db_worker
    return None


# Delete a worker
def delete_worker(db: Session, worker_id: int):
    db_worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if db_worker:
        db.delete(db_worker)
        db.commit()
        return db_worker
    return None
