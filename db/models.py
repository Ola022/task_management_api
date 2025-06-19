from .database  import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Time
from sqlalchemy.orm import relationship

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
    
    
    
class TblTasks(Base):
    __tablename__ = 'tbl_tasks'
    id = Column(Integer, primary_key=True, index=True)    
    title = Column(String)                  #Task title
    description = Column(String)            #Task body
    types = Column(String)                  #Task type: Task / Meeting / Event
    assignee_id = Column(Integer)           #Who is responsible
    assignor_id = Column(Integer)           #Who is reporting the task
    story_point = Column(String)            #Complexity or effort estimation
    priority = Column(String)               # Low / Medium / High / Critical
    status	 = Column(String)               #Pending / In Progress / Done
    created_at = Column(String)             
    due_date = Column(String)
    #user_id  = Column(Integer, ForeignKey('user.id'))
    #user  = relationship('DbUser', back_populates='items')   
    
    
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
    