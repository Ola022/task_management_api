from fastapi import status
from sqlalchemy.orm import Session
from db.models import TblUsers, TblTasks, TblComments
from routers.schemas import TasksBase, TasksDisplay
import datetime
class TaskController:

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
    
    def create_task(self, request: TasksBase):
        new_task = TblTasks(
            name = request.title,
            description = request.description,
            assignee_id = request.assignee_id,
            reporter_id = self.user_info.id,
            story_point = request.story_point,
            priority = request.priority,
            types = request.types,
            status = "Pending",
            due_date = request.due_date,
            created_at = datetime.datetime.now()
        )
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)

        return self.response_success("Task created", {"task_id": new_task.id})

    def update_task(self, task_id: int, request: TasksBase):
        task = self.db.query(TblTasks).filter(TblTasks.id == task_id).first()
        if not task:
            return self.response_error("Task not found", status.HTTP_404_NOT_FOUND)

        if task.reporter_id != self.user_info.id:
            return self.response_error("Only reporter can update this task", status.HTTP_403_FORBIDDEN)

        task.title = request.title
        task.description = request.description
        task.assignee_id = request.assignee_id
        task.story_point = request.story_point
        task.priority = request.priority
        task.types = request.types
        task.status = request.status
        task.due_date = request.due_date

        self.db.commit()
        return self.response_success("Task updated successfully", {"task_id": task.id})
    

    def get_tasks_by_status(self, status: str):
        tasks = self.db.query(TblTasks).filter(TblTasks.status == status).all()
        return self.response_success(f"Tasks with status '{status}'", {"tasks": tasks})
    

    def get_my_tasks(self):
        tasks = self.db.query(TblTasks).filter(TblTasks.assignee_id == self.user_info.id).all()
        return self.response_success("Tasks retrieved", {"tasks": tasks})

    def get_tasks_by_type(self, task_type: str):
        valid_types = ["Meeting", "Event", "Task"]
        if task_type not in valid_types:
            return self.response_error("Invalid task type", status.HTTP_400_BAD_REQUEST)

        tasks = self.db.query(TblTasks).filter(TblTasks.type == task_type).all()
        return self.response_success(f"Tasks of type '{task_type}'", {"tasks": tasks})

    def update_task_status(self, task_id: int, new_status: str):
        task = self.db.query(TblTasks).filter(TblTasks.id == task_id).first()
        if not task:
            return self.response_error("Task not found", status.HTTP_404_NOT_FOUND)

        if task.assignee_id != self.user_info.id:
            return self.response_error("You are not allowed to update this task", status.HTTP_403_FORBIDDEN)

        task.status = new_status
        self.db.commit()
        return self.response_success("Task status updated", {"task_id": task.id, "new_status": task.status})
    

    def get_task_detail(self, task_id: int):
        task = self.db.query(TblTasks).filter(TblTasks.id == task_id).first()
        if not task:
            return self.response_error("Task not found", status.HTTP_404_NOT_FOUND)

        return self.response_success("Task detail fetched", {"task": task})


    def delete_task(self, task_id: int):
        task = self.db.query(TblTasks).filter(TblTasks.id == task_id).first()
        if not task:
            return self.response_error("Task not found", status.HTTP_404_NOT_FOUND)

        if task.reporter_id != self.user_info.id:
            return self.response_error("Only reporter can delete this task", status.HTTP_403_FORBIDDEN)

        self.db.delete(task)
        self.db.commit()
        return self.response_success("Task deleted")

    
    def assign_new_user(self, task_id: int, new_user_id: int):
        task = self.db.query(TblTasks).filter(TblTasks.id == task_id).first()
        if not task:
            return self.response_error("Task not found", status.HTTP_404_NOT_FOUND)

        new_user = self.db.query(TblUsers).filter(TblUsers.id == new_user_id).first()
        if not new_user:
            return self.response_error("New assignee not found", status.HTTP_404_NOT_FOUND)

        task.assignee_id = new_user_id
        self.db.commit()
        return self.response_success("Task reassigned successfully", {"task_id": task_id, "new_assignee_id": new_user_id})
    

    def add_comment_to_task(self, task_id: int, comment_text: str):
        task = self.db.query(TblTasks).filter(TblTasks.id == task_id).first()
        if not task:
            return self.response_error("Task not found", status.HTTP_404_NOT_FOUND)

        comment = TblComments(
            task_id=task_id,
            user_id=self.user_info.id,
            comment=comment_text,
            timestamp=datetime.datetime.now()
        )
        self.db.add(comment)
        self.db.commit()
        return self.response_success("Comment added to task", {"task_id": task_id, "comment": comment_text})
    

    def get_comments_for_task(self, task_id: int):
        task = self.db.query(TblTasks).filter(TblTasks.id == task_id).first()
        if not task:
            return self.response_error("Task not found", status.HTTP_404_NOT_FOUND)

        comments = self.db.query(TblComments).filter(TblComments.task_id == task_id).all()
        return self.response_success("Comments retrieved", {"task_id": task_id, "comments": comments})
    
    def delete_comments(self, comment_id: int):
        comment = self.db.query(TblComments).filter(TblComments.id == comment_id).first()
        if not comment:
            return self.response_error("Comment not found", status.HTTP_404_NOT_FOUND)

        if comment.user_id != self.user_info.id:
            return self.response_error("You are not allowed to delete this comment", status.HTTP_403_FORBIDDEN)

        self.db.delete(comment)
        self.db.commit()
        return self.response_success("Comment deleted")
    
    



