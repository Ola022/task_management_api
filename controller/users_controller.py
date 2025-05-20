import datetime

from db.models import TblUsers
from routers.schemas import UsersBase
from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status
from db.hashing import Hash


def create_user(db: Session, request: UsersBase):
    new_user = TblUsers(        
        full_name = request.full_name,        
        password = Hash.bcrypt(request.password),
        email = request.email,
        role = request.role,
        created_at = datetime.datetime.now(),
        image_url = "none",        
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

   
def get_user_by_id(db: Session, id: int):
    user_info = db.query(TblUsers).filter(TblUsers.id == id).first()
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Recipient account does not exist"
        )
    return {
        "message": "Success",
        "status_code": 200,
        "details": {
            "name": user_info.full_name
        }
    }

   
def get_user_by_email(db: Session, email: int):
    user_info = db.query(TblUsers).filter(TblUsers.email == email).first()
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Recipient account does not exist"
        )
    return {
        "message": "Success",
        "status_code": 200,
        "details": {
            "name": user_info.full_name
        }
    }

def get_user_by_email_for_login(db: Session, email: int):
    return db.query(TblUsers).filter(TblUsers.email == email).first()