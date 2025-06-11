from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from controller.tasks_controller import TaskController
from routers.schemas import TasksBase


router = APIRouter(
    prefix="/task", 
    tags=["Task"]
    )


# Create a new task
@router.post("/create/{user_id}")
def create_task(user_id: int, request: TasksBase, db: Session = Depends(get_db)):
    return TaskController(db, user_id).create_task(request)

# Get tasks by status (e.g. "in-progress", "completed")
@router.get("/status/{status}/{user_id}")
def get_tasks_by_status(status: str, user_id: int, db: Session = Depends(get_db)):
    return TaskController(db, user_id).get_tasks_by_status(status)

# Get tasks assigned to me
@router.get("/mine/{user_id}")
def get_my_tasks(user_id: int, db: Session = Depends(get_db)):
    return TaskController(db, user_id).get_my_tasks()

# Get All tasks 
@router.get("/all/{user_id}")
def get_my_tasks(user_id: int, db: Session = Depends(get_db)):
    return TaskController(db, user_id).get_all_tasks()    

# Get tasks by type (e.g. "Meeting", "Event", "Task")
@router.get("/type/{task_type}/{user_id}")
def get_tasks_by_type(task_type: str, user_id: int, db: Session = Depends(get_db)):
    return TaskController(db, user_id).get_tasks_by_type(task_type)

# Get details for a single task
@router.get("/detail/{task_id}/{user_id}")
def get_task_detail(task_id: int, user_id: int, db: Session = Depends(get_db)):
    return TaskController(db, user_id).get_task_detail(task_id)

# Update task details
@router.put("/update/{task_id}/{user_id}")
def update_task(task_id: int, request: TasksBase, user_id: int, db: Session = Depends(get_db)):
    return TaskController(db, user_id).update_task(task_id, request)

# Update task status (e.g. change from "pending" to "completed")
@router.put("/status/update/{task_id}/{new_status}/{user_id}")
def update_task_status(task_id: int, new_status: str, user_id: int, db: Session = Depends(get_db)):
    return TaskController(db, user_id).update_task_status(task_id, new_status)

# Reassign task to another user
@router.put("/reassign/{task_id}/{new_user_id}/{user_id}")
def assign_new_user(task_id: int, new_user_id: int, user_id: int, db: Session = Depends(get_db)):
    return TaskController(db, user_id).assign_new_user(task_id, new_user_id)

# Delete a task
@router.delete("/delete/{task_id}/{user_id}")
def delete_task(task_id: int, user_id: int, db: Session = Depends(get_db)):
    return TaskController(db, user_id).delete_task(task_id)

# Add a comment to task
@router.post("/comment/add/{task_id}/{user_id}")
def add_comment_to_task(task_id: int, user_id: int, comment_text: str, db: Session = Depends(get_db)):
    return TaskController(db, user_id).add_comment_to_task(task_id, comment_text)

# Get all comments for a task
@router.get("/comment/all/{task_id}/{user_id}")
def get_comments_for_task(task_id: int, user_id: int, db: Session = Depends(get_db)):
    return TaskController(db, user_id).get_comments_for_task(task_id)

# Delete a comment from a task
@router.delete("/comment/delete/{comment_id}/{user_id}")
def delete_comment(comment_id: int, user_id: int, db: Session = Depends(get_db)):
    return TaskController(db, user_id).delete_comments(comment_id)