from pydantic import BaseModel, model_validator, root_validator
from datetime import datetime
from sqlalchemy import DateTime
from typing import List, Optional
from datetime import date, time

#BASE_URL = "https://taskmanagementapi-production-d6fa.up.railway.app"   # change in production
BASE_URL = "http://127.0.0.1:8000"   # change in production
STATIC_PATH = "/static/uploads/projects/"
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
    description:  Optional[str] = None
    types:  Optional[str] = None
    assignee_id: int
    assignor_id: int
    story_point:  Optional[str] = None
    priority:  Optional[str] = None
    status:  Optional[str] = None    
    due_date: str
    class Config():
        from_attributes = True  # replaces orm_mod

#---------------- PROJECT SCHEMAS ----------------
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None    
    due_date: Optional[str] = None
    updated_at: Optional[str] = None
    status: Optional[str] = None


class ProjectDisplay(BaseModel):
    id: int
    name: str
    description: Optional[str]= None
    owner_id: int
    created_at:  Optional[str] = None
    due_date:  Optional[str] = None
    updated_at: Optional[str] = None
    status: Optional[str] = None
    image: Optional[str]
    image_url: Optional[str] = None
    tasks: List[TasksDisplay] = []          # Nested tasks
    class Config:
        from_attributes = True
    
    @model_validator(mode="after")
    def add_image_url(self):
        if self.image:
            self.image_url = f"{BASE_URL}{STATIC_PATH}{self.image}"
        return self
        
class ProjectLightDisplay(BaseModel): # Light version (no tasks)
    id: int
    name: str
    description: Optional[str]= None
    owner_id: int
    created_at:  Optional[str] = None
    due_date:  Optional[str] = None
    updated_at: Optional[str] = None
    image: Optional[str]
    image_url: Optional[str] = None
    status: Optional[str] = None
    class Config:
        from_attributes = True

    @model_validator(mode="after")
    def add_image_url(self):
        if self.image:
            self.image_url = f"{BASE_URL}{STATIC_PATH}{self.image}"
        return self

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
