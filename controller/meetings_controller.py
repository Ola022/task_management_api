from fastapi import status
from sqlalchemy.orm import Session
from db.models import TblMeetings, TblUsers
from routers.schemas import MeetingBase
from typing import List
import datetime

class MeetingController:

    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_info = db.query(TblUsers).filter(TblUsers.id == user_id).first()
        if not self.user_info:
            self.response_error("User not found", status.HTTP_404_NOT_FOUND)

    def response_success(self, message: str, data: dict = {}):
        return {
            "message": "Success",
            "status_code": 200,
            "data": {**data, "message": message},
        }

    def response_error(self, error: str, status_code: int):
        return {
            "message": "Failed",
            "status_code": status_code,
            "data": {"error": error},
        }
    
    def compute_status(self, meeting):
        now = datetime.datetime.now()
        meeting_datetime = datetime.datetime.combine(meeting.date, meeting.time)
        old_status = meeting.status

        if old_status == "Cancelled":
            return "Cancelled"
        if old_status == "Completed":
            return "Completed"

        if now < meeting_datetime:
            new_status = "Upcoming"
        elif now >= meeting_datetime and now.date() == meeting.date.date():
            new_status = "Ongoing"
        elif now.date() > meeting.date.date():
            new_status = "Completed"
        else:
            new_status = old_status

        if old_status != new_status:
            meeting.status = new_status
            self.db.commit()
        return new_status
        
    def create_meeting(self, request: MeetingBase):
        new_meeting = TblMeetings(
            title=request.title,
            agenda=request.agenda,
            organizer=request.organizer,
            participant=",".join(request.participants),
            locationType=request.locationType,
            types=request.types,
            url=request.url,
            venue=request.venue,
            status=request.status,
            date=request.date,
            time=request.time,
        )
        self.db.add(new_meeting)
        self.db.commit()
        self.db.refresh(new_meeting)
        return self.response_success("Meeting created", {"meeting_id": new_meeting.id})

    def get_all_meetings(self):
        meetings = self.db.query(TblMeetings).all()
        # Convert participant string to list for each meeting
        meetings_data = []
        for m in meetings:
            status = self.compute_status(m)
            meetings_data.append({
                "id": m.id,
                "title": m.title,
                "agenda": m.agenda,
                "organizer": m.organizer,
                "participants": m.participant.split(",") if m.participant else [],
                "locationType": m.locationType,
                "types": m.types,
                "url": m.url,
                "venue": m.venue,
                "status": status,
                "date": m.date,
                "time": m.time,
            })
        return self.response_success("Meetings retrieved", {"meetings": meetings_data})

    def get_meeting_detail(self, meeting_id: int):
        m = self.db.query(TblMeetings).filter(TblMeetings.id == meeting_id).first()
        if not m:
            return self.response_error("Meeting not found", status.HTTP_404_NOT_FOUND)
        status = self.compute_status(m)
        meeting_data = {
            "id": m.id,
            "title": m.title,
            "agenda": m.agenda,
            "organizer": m.organizer,
            "participants": m.participant.split(",") if m.participant else [],
            "locationType": m.locationType,
            "types": m.types,
            "url": m.url,
            "venue": m.venue,
            "status": status,
            "date": m.date,
            "time": m.time,
        }
        return self.response_success("Meeting detail fetched", {"meeting": meeting_data})
    
    def update_meeting_status(self, meeting_id: int, new_status: str):
        meeting = self.db.query(TblMeetings).filter(TblMeetings.id == meeting_id).first()
        if not meeting:
            return self.response_error("Meeting not found", status.HTTP_404_NOT_FOUND)
        if new_status not in ["Upcoming", "Ongoing", "Completed", "Cancelled"]:
            return self.response_error("Invalid status", status.HTTP_400_BAD_REQUEST)
        meeting.status = new_status
        self.db.commit()
        return self.response_success("Meeting status updated", {"meeting_id": meeting.id, "new_status": meeting.status})

    def update_meeting(self, meeting_id: int, request: MeetingBase):
        meeting = self.db.query(TblMeetings).filter(TblMeetings.id == meeting_id).first()
        if not meeting:
            return self.response_error("Meeting not found", status.HTTP_404_NOT_FOUND)
        # Optionally, check if only the creator can update
        meeting.title = request.title
        meeting.agenda = request.agenda
        meeting.organizer = request.organizer
        meeting.participant = ",".join(request.participants)
        meeting.locationType = request.locationType
        meeting.types = request.types
        meeting.url = request.url
        meeting.venue = request.venue
        meeting.status = request.status
        meeting.date = request.date
        meeting.time = request.time
        self.db.commit()
        return self.response_success("Meeting updated successfully", {"meeting_id": meeting.id})

    def delete_meeting(self, meeting_id: int):
        meeting = self.db.query(TblMeetings).filter(TblMeetings.id == meeting_id).first()
        if not meeting:
            return self.response_error("Meeting not found", status.HTTP_404_NOT_FOUND)
        self.db.delete(meeting)
        self.db.commit()
        return self.response_success("Meeting deleted")