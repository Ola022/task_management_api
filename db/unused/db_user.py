import datetime

from fastapi import HTTPException, status
from db.models import DbUser
from routers.schemas import UserBase
from sqlalchemy.orm.session import Session
from db.hashing import Hash

def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        surname = request.surname,
        other_name = request.other_name,
        phone_number = request.phone_number,
        password = Hash.bcrypt(request.password),
        email = request.email,
        money = request.money,
        timestamp = datetime.datetime.now(),
        image_url = "none",
        account_number = int(request.phone_number)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_email(db: Session, email: str):
    return db.query(DbUser).filter(DbUser.email == email).first()
   
   
def get_user_by_accountnum(db: Session, account_number: int):
    user_info = db.query(DbUser).filter(DbUser.account_number == account_number).first()
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Recipient account does not exist"
        )
    return {
        "message": "Success",
        "status_code": 200,
        "details": {
            "balance": user_info.money
        }
    }

def get_user_by_phone(db: Session, phone_number: str):
    user_info = db.query(DbUser).filter(DbUser.phone_number == phone_number).first()
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User with this phone number does not exist"
        )
    return {
        "message": "Success",
        "status_code": 200,
        "details": {
            "user_info": user_info
        }
    }


