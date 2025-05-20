from pydantic import BaseModel
from datetime import datetime

class UsersBase(BaseModel):       
    full_name : str
    email : str
    password : str
    role : str
    created_at : datetime
    image_url : str    


class UsersDisplay(BaseModel):
    full_name : str
    email : str    
    role : str
    created_at : str
    image_url : str    
    class Config():
        orm_mode = True
        
        
class TasksBase(BaseModel):     
    title: str
    description: str
    types: str
    assignee_id: int
    reporter_id: int
    story_point: str
    priority: str
    status: str
    created_at: datetime
    due_date: datetime
    
    
class TasksDisplay(BaseModel):
    title: str
    description: str
    types: str
    assignee_id: int
    reporter_id: int
    story_point: str
    priority: str
    status: str    
    due_date: datetime
    class Config():
        orm_mode = True
        
class Comments(BaseModel):        
    task_id: int
    user_id : int
    comment : str
    created_at :datetime
     