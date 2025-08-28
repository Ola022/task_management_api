from fastapi import status
from sqlalchemy.orm import Session
from db.models import TblUsers, TblProjects
from routers.schemas import ProjectBase, ProjectDisplay, ProjectLightDisplay
from pathlib import Path
import shutil
import os, uuid, time
from fastapi import UploadFile
from datetime import datetime

UPLOAD_DIR = Path("static/uploads/projects")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

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

    def create_project(self, request: ProjectBase,  image: UploadFile = None):
         # save image if provided
        filename = None
        if image:
            ext = os.path.splitext(image.filename)[1]  # keep original extension
            filename = f"{int(time.time())}_{uuid.uuid4().hex}{ext}"
            filepath = UPLOAD_DIR / filename
                        
            with open(filepath, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)

        new_project = TblProjects(
            name=request.name,
            description=request.description,
            owner_id=self.user_info.id,
            created_at=datetime.utcnow().isoformat(),  
            updated_at=datetime.utcnow().isoformat(),
            due_date=request.due_date,
            status="active",
            image=filename
        )
        self.db.add(new_project)
        self.db.commit()
        self.db.refresh(new_project)

        return self.response_success("Project created",     
                                     {"project": ProjectLightDisplay.model_validate(new_project)}
)

    def get_project(self, project_id: int):
        project = self.db.query(TblProjects).filter(TblProjects.id == project_id).first()
        if not project:
            return self.response_error("Project not found", status.HTTP_404_NOT_FOUND)

        return self.response_success("Project fetched", {"project": ProjectLightDisplay.model_validate(project)})
    
    def get_all_projects(self, include_tasks: bool = False):
        projects = self.db.query(TblProjects).all()

        if include_tasks:
            return self.response_success(
                "Projects with tasks fetched",
                {"projects": [ProjectDisplay.model_validate(p) for p in projects]}
            )
        
        return self.response_success(
            "Projects fetched",
            {"projects": [ProjectLightDisplay.model_validate(p) for p in projects]})

    #def get_all_projects(self):
    #    projects = self.db.query(TblProjects).all()
    #    return self.response_success("Projects fetched", {"projects": projects})
    def update_project(self, project_id: int, name: str = None, description: str = None,
                   due_date: str = None, status: str = None, image: UploadFile = None):
        project = self.db.query(TblProjects).filter(TblProjects.id == project_id).first()
        if not project:
            return self.response_error("Project not found", status.HTTP_404_NOT_FOUND)

        # Update only provided fields
        if name is not None:
            project.name = name
        if description is not None:
            project.description = description
        if due_date is not None:
            project.due_date = due_date
        if status is not None:
            project.status = status

        # Handle image update
        if image:
            ext = os.path.splitext(image.filename)[1]
            filename = f"{int(time.time())}_{uuid.uuid4().hex}{ext}"
            filepath = UPLOAD_DIR / filename

            with open(filepath, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)

            # Remove old image if exists
            if project.image:
                old_path = UPLOAD_DIR / project.image
                if old_path.exists():
                    old_path.unlink()

            project.image = filename

        project.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(project)

        return self.response_success("Project updated", {"project_id": project.id})
    
    def update_project_status(self, project_id: int, new_status: str):
        project = self.db.query(TblProjects).filter(TblProjects.id == project_id).first()
        if not project:
            return self.response_error("Project not found", status.HTTP_404_NOT_FOUND)
        if new_status not in ["active", "inactive"]:
            return self.response_error("Invalid status", status.HTTP_400_BAD_REQUEST)
        project.status = new_status
        self.db.commit()
        return self.response_success("Project updated", {"project_id": project.id})


    def get_projects_by_status(self, status: str, include_tasks: bool = False):
        query = self.db.query(TblProjects)

        if status:
            query = query.filter(TblProjects.status == status.lower())
        projects = query.all()

        if include_tasks:
            return self.response_success(
                "Projects with tasks fetched",
                {"projects": [ProjectDisplay.model_validate(p) for p in projects]}
            )

        return self.response_success(
            "Projects fetched",
            {"projects": [ProjectLightDisplay.model_validate(p) for p in projects]}
        )
    
    def update_project_image(self, project_id: int, image: UploadFile):
        project = self.db.query(TblProjects).filter(TblProjects.id == project_id).first()
        if not project:
            return self.response_error("Project not found", status.HTTP_404_NOT_FOUND)

        ext = os.path.splitext(image.filename)[1]
        filename = f"{int(time.time())}_{uuid.uuid4().hex}{ext}"
        filepath = UPLOAD_DIR / filename

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        if project.image:
            old_path = UPLOAD_DIR / project.image
            if old_path.exists():
                old_path.unlink()

        project.image = filename
        project.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(project)

        return self.response_success("Image updated", {"image": filename})


    def delete_project(self, project_id: int):
        project = self.db.query(TblProjects).filter(TblProjects.id == project_id).first()
        if not project:
            return self.response_error("Project not found", status.HTTP_404_NOT_FOUND)
        if project.image:
            filepath = UPLOAD_DIR / project.image
            if filepath.exists():
                filepath.unlink()  # deletes the file safely

        self.db.delete(project)
        self.db.commit()

        return self.response_success("Project deleted", {"project_id": project_id})

    
