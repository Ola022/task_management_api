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

@router.post("/signup", response_model=UsersDisplay)
def create_user(request: UsersBase, db: Session = Depends(get_db)):
    return users_controller.create_user(db, request)

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
        "data": {
            "user_info": user
        }
    }
    

#@router.get("/verify_user/{account_number}")
#def check_balance(account_number: int, db: Session = Depends(get_db)):
#    account = db_user.get_user_by_accountnum(db, account_number)
#    return account