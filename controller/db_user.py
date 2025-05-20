import datetime

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
    return db.query(DbUser).filter(DbUser.account_number == account_number).first()


def get_user_by_phone(db: Session, phone_number: str):
    return db.query(DbUser).filter(DbUser.phone_number == phone_number).first()


