from fastapi import APIRouter, Depends, Query,  Form, File, UploadFile
from sqlalchemy.orm import Session
from db.database import get_db
from controller.projects_controller import ProjectController
from routers.schemas import ProjectBase, ProjectDisplay

router = APIRouter(
    prefix="/project",
    tags=["Projects"]
)


# Create a new project
@router.post("/create/{user_id}")
#def create_project(user_id: int, request: ProjectBase, db: Session = Depends(get_db)):
#    return ProjectController(db, user_id).create_project(request)
def create_project(
    user_id: int,
    name: str = Form(...),
    description: str = Form(None),
    due_date: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    request = ProjectBase(
        name=name,
        description=description,
        due_date=due_date
    )
    return ProjectController(db, user_id).create_project(request, image)



# Get single project by id
@router.get("/{user_id}/{project_id}")
def get_project(user_id: int, project_id: int, db: Session = Depends(get_db)):
    return ProjectController(db, user_id).get_project(project_id)


# Get all projects (optionally include tasks)
@router.get("/all")
def get_all_projects(user_id: int, include_tasks: bool = False, db: Session = Depends(get_db)):
    return ProjectController(db, user_id).get_all_projects(include_tasks)


# Update a project
#@router.put("/update/{user_id}/{project_id}")
#def update_project(user_id: int, project_id: int, request: ProjectBase, db: Session = Depends(get_db)):
#    return ProjectController(db, user_id).update_project(project_id, request)
@router.put("/update/{user_id}/{project_id}")
def update_project(
    user_id: int,
    project_id: int,
    name: str = Form(None),
    description: str = Form(None),
    due_date: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    return ProjectController(db, user_id).update_project(
        project_id,
        name=name,
        description=description,
        due_date=due_date,
        image=image
    )


@router.put("/{project_id}/image")
def update_project_image(project_id: int, image: UploadFile = File(...), db: Session = Depends(get_db)):
    return ProjectController(db, None).update_project_image(project_id, image)

# Delete a project
@router.delete("/delete/{user_id}/{project_id}")
def delete_project(user_id: int, project_id: int, db: Session = Depends(get_db)):
    return ProjectController(db, user_id).delete_project(project_id)


# Get project with its tasks
@router.get("/with-tasks/{user_id}/{project_id}")
def get_project_with_tasks(user_id: int, project_id: int, db: Session = Depends(get_db)):
    return ProjectController(db, user_id).get_project_with_tasks(project_id)
