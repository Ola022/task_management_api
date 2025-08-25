# routers/metrics.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controller.metric_controller import MetricController
from db.database import get_db


router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"]
)

@router.get("/{user_id}")
def get_metrics( user_id: int, db: Session = Depends(get_db)):
    return MetricController(db,).get_metrics( user_id)