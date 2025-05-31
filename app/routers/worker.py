from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.worker import create_worker, get_worker, get_workers, update_worker, delete_worker
from app.schemas.worker import WorkerCreate, WorkerUpdate, Worker
from app.utils.jwt_auth import get_worker_id_from_token

router = APIRouter(prefix="/workers", tags=["Workers"])


# Create worker
@router.post("/", response_model=Worker)
def create_worker_route(worker: WorkerCreate, db: Session = Depends(get_db)):
    return create_worker(db=db, worker=worker)


# Get worker by id
@router.get("/{worker_id}", response_model=Worker)
def get_worker_route(worker_id: int, db: Session = Depends(get_db)):
    db_worker = get_worker(db=db, worker_id=worker_id)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker


# get connected worker by id
@router.get("/connected_worker", response_model=Worker)
def get_connected_worker_route(worker_id: int = Depends(get_worker_id_from_token), db: Session = Depends(get_db)):
    db_worker = get_worker(db=db, worker_id=worker_id)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker


# Get all workers
@router.get("/", response_model=List[Worker])
def get_workers_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_workers(db=db, skip=skip, limit=limit)


# Update worker
@router.put("/{worker_id}", response_model=Worker)
def update_worker_route(worker_id: int, worker: WorkerUpdate, db: Session = Depends(get_db)):
    db_worker = update_worker(db=db, worker_id=worker_id, worker=worker)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker


# Update connected worker
@router.put("/connected", response_model=Worker)
def update_worker_route(worker: WorkerUpdate, worker_id: int = Depends(get_worker_id_from_token),
                        db: Session = Depends(get_db)):
    db_worker = update_worker(db=db, worker_id=worker_id, worker=worker)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker


# Delete worker
@router.delete("/{worker_id}", response_model=Worker)
def delete_worker_route(worker_id: int, db: Session = Depends(get_db)):
    db_worker = delete_worker(db=db, worker_id=worker_id)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker
