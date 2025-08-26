from fastapi import status
from sqlalchemy.orm import Session
from db.models import TblUsers, TblTasks, TblComments, TblProjects
from routers.schemas import TasksBase, TasksDisplay
import datetime

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
    
    def send_email(self, to_email: str, subject: str, body: str, request):
        # Configure your SMTP server and credentials        
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        body = body + f""" Here are the details: 
Title: {request.title} 
Description: {request.description}
Assigned By: {self.user_info.full_name}
Story Point: {request.story_point}
Priority: {request.priority}                        
Due Date: {request.due_date}

Please log in to your dashboard for more information and to begin working on this task.
Thank you,
https://taskmanagementwebapps.netlify.app/

Faculty of Computing and Informatics - Task Management System."""
        #smtp_user = "orlam0222@gmail.com" #ajnd ooah ddkd pant
        #smtp_password = "ajndooahddkdpant"  #`ajnd ooah ddkd pant` 16-char app password, no spaces
        smtp_user = "orlamtesting0222@gmail.com" 
        smtp_password = "tohksrovckqvqjrk"  #`tohk srov ckqv qjrk` 16-char app password, no spaces
        
        msg = MIMEMultipart()
        msg["From"] = smtp_user
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, to_email, msg.as_string())
            print(f"send email to {to_email}")
            server.quit()
        except Exception as e:
            print(f"Failed to send email: {e}")

    def create_task(self, request: TasksBase):
          # Check project exists
        project = self.db.query(TblProjects).filter(TblProjects.id == request.project_id).first()
        if not project:
            return self.response_error("Project not found", status.HTTP_404_NOT_FOUND)

        new_task = TblTasks(
            project_id = request.project_id,    # <<< NEW
            title = request.title,
            description = request.description,
            assignee_id = request.assignee_id,
            assignor_id = self.user_info.id,
            story_point = request.story_point,
            priority = request.priority,
            types = request.types,
            status = request.status, #"Pending",
            due_date = request.due_date,
            created_at = request.created_at, #datetime.datetime.now()
        )
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)

          # Fetch and update assignee through  email
        assignee = self.db.query(TblUsers).filter(TblUsers.id == request.assignee_id).first()
        if assignee and assignee.email:
            subject = "New Task Assigned: " + new_task.title.upper()
            body = f""" \n Hello {assignee.full_name.upper()}, \nYou have been assigned a new task. """
            #body = f"Hello {assignee.full_name},\n\nYou have been assigned a new task: '{new_task.title}'."
            self.send_email(assignee.email, subject, body, request)

        return self.response_success("Task created", {"task_id": new_task.id})

    def update_task(self, task_id: int, request: TasksBase):
        task = self.db.query(TblTasks).filter(TblTasks.id == task_id).first()
        if not task:
            return self.response_error("Task not found", status.HTTP_404_NOT_FOUND)

        if task.assignor_id != self.user_info.id:
            return self.response_error("Only Assignor can update this task", status.HTTP_403_FORBIDDEN)
         # Validate project if updated
        if request.project_id:
            project = self.db.query(TblProjects).filter(TblProjects.id == request.project_id).first()
            if not project:
                return self.response_error("Project not found", status.HTTP_404_NOT_FOUND)
        task.project_id = request.project_id 
        task.title = request.title
        task.description = request.description
        task.assignee_id = request.assignee_id
        task.story_point = request.story_point
        task.priority = request.priority
        task.types = request.types
        task.status = request.status
        task.due_date = request.due_date

        self.db.commit()
        # Fetch assignee email
        assignee = self.db.query(TblUsers).filter(TblUsers.id == request.assignee_id).first()
        if assignee and assignee.email:
            subject = "Task Updated"
            body = f"Hello {assignee.full_name.upper()},\n\n The task: '{request.title.upper()}', As been updated."
            self.send_email(assignee.email, subject, body, request)
        # Fetch assignor email
        assignor = self.db.query(TblUsers).filter(TblUsers.id == request.assignor_id).first()
        if assignor and assignor.email:
            subject = "You just Update Task : " +  request.title
            body = f""" \n Hello {assignor.full_name.upper()}, \n  Your task as been updated successfully """            
            self.send_email(assignor.email, subject, body, request)
        return self.response_success("Task updated successfully", {"task_id": task.id})
    
    def get_tasks_by_status(self, project_id: int, status: str):
        tasks = self.db.query(TblTasks).filter(
            TblTasks.status == status,
            TblTasks.project_id == project_id
        ).all()
        return self.response_success(f"Tasks with status '{status}'", {"tasks": tasks})

    #def get_tasks_by_status(self, status: str):
    #    tasks = self.db.query(TblTasks).filter(TblTasks.status == status).all()
    #    return self.response_success(f"Tasks with status '{status}'", {"tasks": tasks})
    # Get all tasks under a project
    def get_all_tasks(self, project_id: int):
        tasks = self.db.query(TblTasks).filter(TblTasks.project_id == project_id).all()
        return self.response_success("Tasks retrieved", {"tasks": tasks})

    # Get my tasks under a project
    def get_my_tasks(self, project_id: int):
        tasks = self.db.query(TblTasks).filter(
            TblTasks.assignor_id == self.user_info.id,
            TblTasks.project_id == project_id
        ).all()
        return self.response_success("Tasks retrieved", {"tasks": tasks})

# Get tasks by type under a project
    def get_tasks_by_type(self, project_id: int, task_type: str):
        valid_types = ["Meeting", "Event", "Task"]
        if task_type not in valid_types:
            return self.response_error("Invalid task type", status.HTTP_400_BAD_REQUEST)

        tasks = self.db.query(TblTasks).filter(
            TblTasks.project_id == project_id,
            TblTasks.types == task_type
        ).all()
        return self.response_success(f"Tasks of type '{task_type}'", {"tasks": tasks})
    
    def update_task_status(self, task_id: int, new_status: str):
        task = self.db.query(TblTasks).filter(TblTasks.id == task_id).first()
        if not task:
            return self.response_error("Task not found", status.HTTP_404_NOT_FOUND)
        if task.assignee_id != self.user_info.id and task.assignor_id != self.user_info.id :
            return self.response_error("You are not allowed to update this task", status.HTTP_403_FORBIDDEN)

        task.status = new_status
        self.db.commit()

        assignee = self.db.query(TblUsers).filter(TblUsers.id == task.assignee_id).first()        
        if assignee and assignee.email:
            subject = "Status Updated"
            body = f"Hi {assignee.full_name.upper()},\n\n The task: '{task.title.upper()}', Status has been updated."
            self.send_email(assignee.email, subject, body, task )
        assignor = self.db.query(TblUsers).filter(TblUsers.id == task.assignor_id).first()
        if assignor and assignor.email:
            subject = "Status Updated"
            body = f"Hello { assignor.full_name.upper()},\n\n The task '{task.title.upper()}', status has been updated"
            self.send_email(assignor.email, subject, body, task)        
        
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

        if task.assignor_id != self.user_info.id:
            return self.response_error("Only assignor can delete this task", status.HTTP_403_FORBIDDEN)

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

        assignee = self.db.query(TblUsers).filter(TblUsers.id == task.assignee_id).first()        
        if assignee and assignee.email:
            subject = "New Task Assigned: " + task.title
            body = f""" \n Hello {assignee.full_name.upper()}, \nYou have been assigned a new task. """
            self.send_email(assignee.email, subject, body, task)
        assignor = self.db.query(TblUsers).filter(TblUsers.id == task.assignor_id).first()
        if assignor and assignor.email:
            subject = "Task re-Assigned Successfully"
            body = f"Hello {assignor.full_name.upper()},\n\n Your task '{task.title.upper()}', has been reassign to {assignee.full_name.upper()}"
            self.send_email(assignor.email, subject, body, task)        
        
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
    

    def get_comments_for_taskk(self, task_id: int):
        task = self.db.query(TblTasks).filter(TblTasks.id == task_id).first()
        if not task:
            return self.response_error("Task not found", status.HTTP_404_NOT_FOUND)

        comments = self.db.query(TblComments).filter(TblComments.task_id == task_id).all()
        return self.response_success("Comments retrieved", {"task_id": task_id, "comments": comments})
        
    def get_comments_for_task(self, task_id: int):
        task = self.db.query(TblTasks).filter(TblTasks.id == task_id).first()
        if not task:
            return self.response_error("Task not found", status.HTTP_404_NOT_FOUND)

        comments = (self.db.query(TblComments).filter(TblComments.task_id == task_id).all())

        # Attach full_name to each comment
        comments_with_names = []
        for comment in comments:
            user = self.db.query(TblUsers).filter(TblUsers.id == comment.user_id).first()
            full_name = user.full_name if user else "No Name"
            comments_with_names.append({
                "id": comment.id,
                "task_id": comment.task_id,
                "user_id": comment.user_id,
                "full_name": full_name,
                "comment": comment.comment,
                "timestamp": comment.timestamp.isoformat() if comment.timestamp else None
            })

        return self.response_success("Comments retrieved", {"task_id": task_id, "comments": comments_with_names})
    
    def delete_comments(self, comment_id: int):
        comment = self.db.query(TblComments).filter(TblComments.id == comment_id).first()
        if not comment:
            return self.response_error("Comment not found", status.HTTP_404_NOT_FOUND)

        if comment.user_id != self.user_info.id:
            return self.response_error("You are not allowed to delete this comment", status.HTTP_403_FORBIDDEN)

        self.db.delete(comment)
        self.db.commit()
        return self.response_success("Comment deleted")
    
    



