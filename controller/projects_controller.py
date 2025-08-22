from fastapi import status
from sqlalchemy.orm import Session
from db.models import TblUsers, TblProjects
from routers.schemas import ProjectBase
import datetime


class ProjectController:

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

    # ---------------- CRUD METHODS ----------------

    def create_project(self, request: ProjectBase):
        new_project = TblProjects(
            name=request.name,
            description=request.description,
            owner_id=self.user_info.id,
            created_at=request.created_at,  # or datetime.datetime.now()
            due_date=request.due_date,
        )
        self.db.add(new_project)
        self.db.commit()
        self.db.refresh(new_project)

        return self.response_success("Project created", {"project_id": new_project.id})

    def get_project(self, project_id: int):
        project = self.db.query(TblProjects).filter(TblProjects.id == project_id).first()
        if not project:
            return self.response_error("Project not found", status.HTTP_404_NOT_FOUND)

        return self.response_success("Project fetched", {"project": project})

    def get_all_projects(self):
        projects = self.db.query(TblProjects).all()
        return self.response_success("Projects fetched", {"projects": projects})

    def update_project(self, project_id: int, request: ProjectBase):
        project = self.db.query(TblProjects).filter(TblProjects.id == project_id).first()
        if not project:
            return self.response_error("Project not found", status.HTTP_404_NOT_FOUND)

        project.name = request.name
        project.description = request.description
        project.due_date = request.due_date
        project.created_at = request.created_at  # careful if you want to update this

        self.db.commit()
        self.db.refresh(project)

        return self.response_success("Project updated", {"project_id": project.id})

    def delete_project(self, project_id: int):
        project = self.db.query(TblProjects).filter(TblProjects.id == project_id).first()
        if not project:
            return self.response_error("Project not found", status.HTTP_404_NOT_FOUND)

        self.db.delete(project)
        self.db.commit()

        return self.response_success("Project deleted", {"project_id": project_id})

    # ---------------- EXTRA METHODS ----------------

    def get_project_with_tasks(self, project_id: int):
        project = self.db.query(TblProjects).filter(TblProjects.id == project_id).first()
        if not project:
            return self.response_error("Project not found", status.HTTP_404_NOT_FOUND)

        # thanks to relationship in models, tasks are accessible
        return self.response_success("Project and tasks fetched", {
            "project": {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "due_date": project.due_date,
                "tasks": project.tasks
            }
        })
