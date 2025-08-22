from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import DateTime
from typing import List, Optional
from datetime import date, time
class UsersBase(BaseModel):       
    full_name : str
    email : str
    password : str
    role : int
    created_at : str
    title : str
    academic_rank : str
    image_url : str        


class UsersDisplay(BaseModel):
    id: int
    full_name : str
    email : str    
    role : int
    created_at : str   
    title : str
    academic_rank : str 
    image_url : str
    class Config():
        from_attributes = True  # replaces orm_mode
        # orm_mode = True

 #---------------- PROJECT SCHEMAS ----------------
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    owner_id: int
    created_at: str
    due_date: str


class ProjectDisplay(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    created_at: str
    due_date: str
    tasks: List[TasksDisplay] = []          # Nested tasks

    class Config:
        from_attributes = True

        
class TasksBase(BaseModel):    
    project_id: int
    title: str
    description: str
    types: str
    assignee_id: int
    assignor_id: int
    story_point: str
    priority: str
    status: str
    created_at: str
    due_date: str
    
    
class TasksDisplay(BaseModel):
    id: int
    project_id: int
    title: str
    description: str
    types: str
    assignee_id: int
    assignor_id: int
    story_point: str
    priority: str
    status: str    
    due_date: str
    class Config():
        from_attributes = True  # replaces orm_mod
        
class Comments(BaseModel):        
    task_id: int
    user_id : int
    comment : str
    timestamp :datetime    

class MeetingBase(BaseModel):
    title: str
    agenda: Optional[str] = None
    organizer: str
    participants: List[str]
    locationType: str
    types: Optional[str] = None
    url: Optional[str] = None
    venue: Optional[str] = None
    status: str
    date: date
    time: time  # or time if you use Time column


class MeetingDisplay(MeetingBase):
    id: int

    class Config:
        orm_mode = True
