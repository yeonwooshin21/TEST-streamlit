from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.get("/videos", response_model=list[schemas.Video])
def read_videos(db: Session = Depends(get_db)):
    videos = crud.get_videos(db)
    return videos

