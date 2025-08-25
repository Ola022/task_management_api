from .database  import Base
from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text, DateTime, Time
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

class ProjectStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    
class TblUsers(Base):
    __tablename__ = 'tbl_users'
    id = Column(Integer, primary_key=True, index=True)    
    full_name = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(Integer)
    created_at = Column(String)
    title = Column(String)    
    academic_rank = Column(String)      #Prof., Dr., Mr., Ms., Mrs.
    image_url = Column(String)          #Senior Lecturer, Junior Lecturer, Lecturer I, Lecturer II
    projects = relationship(
        "TblProjects",
        back_populates="owner",
        cascade="all, delete-orphan"
    )
    
class TblProjects(Base):
    __tablename__ = "tbl_projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)                           # Project name
    description = Column(Text, nullable=True)                       # Project details
    status = Column(Enum(ProjectStatus), default=ProjectStatus.active)   # ✅ new column
    owner_id = Column(Integer, ForeignKey("tbl_users.id"))          # Who owns/created the project
    created_at = Column(String, nullable=True)
    due_date = Column(String, nullable=True)
    updated_at  = Column(String, nullable=True)
    image = Column(String, nullable=True)                           # store filename or URL

    # Relationship: one project -> many tasks
    tasks = relationship("TblTasks", back_populates="project", cascade="all, delete-orphan")
    owner = relationship("TblUsers", back_populates="projects")


class TblTasks(Base):
    __tablename__ = 'tbl_tasks'
    id = Column(Integer, primary_key=True, index=True)    
    project_id = Column(Integer, ForeignKey("tbl_projects.id", ondelete="CASCADE"))  # Link to project
    
    title = Column(String)                  #Task title
    description = Column(String)            #Task body
    types = Column(String)                  #Task type: Task / Meeting / Event
    assignee_id = Column(Integer)           #Who is responsible
    assignor_id = Column(Integer)           #Who is reporting the task
    story_point = Column(String)            #Complexity or effort estimation
    priority = Column(String)               #Low / Medium / High / Critical
    status	 = Column(String)               #Pending / In Progress / Done
    created_at = Column(String)             
    due_date = Column(String)

    # Relationship back to project
    project = relationship("TblProjects", back_populates="tasks")    
    
    
class TblComments(Base):
    __tablename__ = 'tbl_comments'
    id = Column(Integer, primary_key=True, index=True)    
    task_id = Column(Integer)  
    user_id = Column(Integer)  
    comment = Column(String)
    timestamp = Column(DateTime)    
    
class TblMeetings(Base):
    __tablename__ = 'tbl_meetings'
    id = Column(Integer, primary_key=True, index=True)    
    title = Column(String)  
    agenda = Column(String)  
    organizer = Column(String)
    participant = Column(String)    
    locationType = Column(String)
    types = Column(String)
    url = Column(String)
    venue = Column(String)
    status = Column(String)
    date = Column(DateTime)
    time = Column(Time)  
    
