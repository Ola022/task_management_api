import datetime
from routers.schemas import PostBase
from sqlalchemy.orm.session import Session
from db.models import DbPost

def create(db: Session, request: PostBase):
    new_post = DbPost(
        image_url = request.image_url,
        image_url_type = request.image_url_type,
        description = request.description,
        timestamp = datetime.datetime.now(),
        user_id = request.user_id        
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_all(db: Session):
    return db.query(DbPost).all()