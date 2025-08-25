# controllers/metricController.py
from fastapi import status
from sqlalchemy.orm import Session
from db.models import TblProjects, TblTasks
from datetime import datetime

class MetricController:
    def __init__(self, db: Session):
        self.db = db

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

    def get_metrics(self, user_id: int):
        try:
            # --- Overall ---
            total_projects = self.db.query(TblProjects).count()
            active_projects = self.db.query(TblProjects).filter(TblProjects.status == "active").count()
            inactive_projects = self.db.query(TblProjects).filter(TblProjects.status == "inactive").count()

            total_tasks = self.db.query(TblTasks).count()
            completed_tasks = self.db.query(TblTasks).filter(TblTasks.status == "Completed").count()
            pending_tasks = self.db.query(TblTasks).filter(TblTasks.status == "Progress").count()

            # --- Per Project Breakdown ---
            projects_data = []
            projects = self.db.query(TblProjects).all()
            for project in projects:
                tasks = self.db.query(TblTasks).filter(TblTasks.project_id == project.id).all()

                total = len(tasks)
                completed = len([t for t in tasks if t.status == "Completed"])
                pending = len([t for t in tasks if t.status == "Progress"])
                #overdue = len([t for t in tasks if t.due_date and t.due_date < datetime.utcnow() and t.status != "completed"])                
                overdue = 0
                for t in tasks:
                    if t.due_date and t.status != "Completed":
                        try:
                            due_date = None
                            if isinstance(t.due_date, int):  
                                # If stored as UNIX timestamp
                                due_date = datetime.fromtimestamp(t.due_date)
                            elif isinstance(t.due_date, str):
                                # Try multiple formats
                                for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y"):
                                    try:
                                        due_date = datetime.strptime(t.due_date, fmt)
                                        break
                                    except ValueError:
                                        continue

                            if due_date and due_date < datetime.utcnow():
                                overdue += 1

                        except Exception:
                            # Ignore bad or unparseable values
                            continue
                
                projects_data.append({
                    "id": project.id,
                    "name": project.name,
                    "status": project.status,
                    "totalTasks": total,
                    "completedTasks": completed,
                    "pendingTasks": pending,
                    "overdueTasks": overdue,
                })
             
             # --- User Specific ---
            user_tasks = self.db.query(TblTasks).filter(TblTasks.assignee_id == user_id).all()
            total_assigned = len(user_tasks)
            completed_me = len([t for t in user_tasks if t.status.lower() == "Completed"])
            pending_me = len([t for t in user_tasks if t.status.lower() in ("Progress", "Pending")])

            overdue_me = 0
            for t in user_tasks:
                if t.due_date and t.status.lower() != "Completed":
                    try:
                        due_date = None
                        if isinstance(t.due_date, int):
                            due_date = datetime.fromtimestamp(t.due_date)
                        elif isinstance(t.due_date, str):
                            for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y"):
                                try:
                                    due_date = datetime.strptime(t.due_date, fmt)
                                    break
                                except ValueError:
                                    continue
                        if due_date and due_date < datetime.utcnow():
                            overdue_me += 1
                    except Exception:
                        continue

            user_metrics = {
                "totalAssignedToMe": total_assigned,
                "completedByMe": completed_me,
                "pendingForMe": pending_me,
                "overdueForMe": overdue_me
            }
            
            return self.response_success("Metrics fetched", {
                "overview": {
                    "totalProjects": total_projects,
                    "activeProjects": active_projects,
                    "inactiveProjects": inactive_projects,
                    "totalTasks": total_tasks,
                    "completedTasks": completed_tasks,
                    "pendingTasks": pending_tasks,
                },
                "projects": projects_data,
                "user": user_metrics

            })

        except Exception as e:
            return self.response_error(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
