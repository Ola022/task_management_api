from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import DateTime

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
    title: str
    description: str
    types: str
    assignee_id: int
    reporter_id: int
    story_point: str
    priority: str
    status: str
    created_at: str
    due_date: str
    
    
class TasksDisplay(BaseModel):
    title: str
    description: str
    types: str
    assignee_id: int
    reporter_id: int
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
    created_at :str
     