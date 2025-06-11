from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.hashing import Hash
from routers.schemas import UsersBase, UsersDisplay
from controller import users_controller

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/signup")
def create_user(request: UsersBase, db: Session = Depends(get_db)):
    user = users_controller.create_user(db, request)
    return {
        "message": "Success",
        "status_code": 200,
        "data": "User added successfully",
        "user": UsersDisplay.model_validate(user)

    }

@router.get("/login")
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    user = users_controller.get_user_by_email_for_login(db, email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, data="User not found")
    
    if not Hash.verify(user.password, password):  # Assuming verify function exists
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, data="Incorrect password")
    
    return {
        "message": "Success",
        "status_code": 200,
        #"data": user
        "data": UsersDisplay.model_validate(user)        
    }
    

@router.get("/all",)
def get_All_Users(db: Session = Depends(get_db)):
    return  users_controller.get_all_users(db)
#@router.get("/all", response_model=List[UsersDisplay])
#def get_all_users(db: Session = Depends(get_db)):
#    users = users_controller.get_all_users(db)
#   return [UsersDisplay.model_validate(user) for user in users]    



#@router.get("/verify_user/{account_number}")
#def check_balance(account_number: int, db: Session = Depends(get_db)):
#    account = db_user.get_user_by_accountnum(db, account_number)
#    return account