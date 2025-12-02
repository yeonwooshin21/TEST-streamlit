# backend/crud.py
from sqlalchemy.orm import Session
from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # ✅ ORM 변환 대신, 명시적으로 dict로 리턴
    return schemas.UserResponse(
        id=db_user.id,
        name=db_user.name,
        email=db_user.email,
        created_at=db_user.created_at
    )

def get_users(db: Session):
    return db.query(models.User).all()

def get_videos(db: Session):
    return db.query(models.Video).all()
