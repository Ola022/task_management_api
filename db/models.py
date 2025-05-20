from .database  import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

class DbUsers(Base):
    __tablename__ = 'tbl_users'
    id = Column(Integer, primary_key=True, index=True)    
    full_name = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(Integer)
    created_at = Column(DateTime)
    image_url = Column(String)    
    
    
    
class DbTasks(Base):
    __tablename__ = 'tbl_tasks'
    id = Column(Integer, primary_key=True, index=True)    
    title = Column(String)                  #Task title
    description = Column(String)            #Task body
    types = Column(String)                  #Task type: Task / Meeting / Event
    assignee_id = Column(Integer)           #Who is responsible
    reporter_id = Column(Integer)           #Who is reporting the task
    story_point = Column(String)            #Complexity or effort estimation
    priority = Column(String)               # Low / Medium / High / Critical
    status	 = Column(String)               #Pending / In Progress / Done
    created_at = Column(DateTime)             
    due_date = Column(DateTime)
    #user_id  = Column(Integer, ForeignKey('user.id'))
    #user  = relationship('DbUser', back_populates='items')   
    
    
class DbComments(Base):
    __tablename__ = 'tbl_comments'
    id = Column(Integer, primary_key=True, index=True)    
    task_id = Column(Integer)  
    user_id = Column(String)  
    comment = Column(String)
    created_at = Column(DateTime)    
    