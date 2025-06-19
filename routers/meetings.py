from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from controller.meetings_controller import MeetingController
from routers.schemas import MeetingBase

router = APIRouter(
    prefix="/meeting",
    tags=["Meeting"]
)

# Create a new meeting
@router.post("/create/{user_id}")
def create_meeting(user_id: int, request: MeetingBase, db: Session = Depends(get_db)):
    return MeetingController(db, user_id).create_meeting(request)

# Get all meetings
@router.get("/all/{user_id}")
def get_all_meetings(user_id: int, db: Session = Depends(get_db)):
    return MeetingController(db, user_id).get_all_meetings()

# Get meeting details
@router.get("/detail/{meeting_id}/{user_id}")
def get_meeting_detail(meeting_id: int, user_id: int, db: Session = Depends(get_db)):
    return MeetingController(db, user_id).get_meeting_detail(meeting_id)

# Update meeting details
@router.put("/update/{meeting_id}/{user_id}")
def update_meeting(meeting_id: int, user_id: int, request: MeetingBase, db: Session = Depends(get_db)):
    return MeetingController(db, user_id).update_meeting(meeting_id, request)

# Update meeting status (manual)
@router.put("/status/update/{meeting_id}/{new_status}/{user_id}")
def update_meeting_status(meeting_id: int, new_status: str, user_id: int, db: Session = Depends(get_db)):
    return MeetingController(db, user_id).update_meeting_status(meeting_id, new_status)

# Delete a meeting
@router.delete("/delete/{meeting_id}/{user_id}")
def delete_meeting(meeting_id: int, user_id: int, db: Session = Depends(get_db)):
    return MeetingController(db, user_id).delete_meeting(meeting_id)