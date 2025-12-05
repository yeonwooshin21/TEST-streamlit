from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import Base, engine, get_db
from .routes import videos, user
from sqlalchemy.orm import Session

# DB 초기화 (테이블 생성)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- CORS 설정 (Streamlit과 연동 가능하도록 허용) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 필요 시 Streamlit 배포 도메인만 허용하도록 수정 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 기본 라우트 (테스트용) ---
@app.get("/")
def read_root():
    return {"message": "🚀 FastAPI + SQLite 연결 성공!"}

# ✅ 유저 관련 API 라우터 연결
app.include_router(user.router)
app.include_router(videos.router)

@app.post("/sample-data")
def insert_sample_data(db: Session = Depends(get_db)):
    # 예시 샘플 데이터 (너의 프로젝트 맞춰서 변경 가능)
    sample_videos = [
        models.Video(
            title="샘플 제목 1",
            description="샘플 설명 1",
            url="http://example.com/1"
        ),
        models.Video(
            title="샘플 제목 2",
            description="샘플 설명 2",
            url="http://example.com/2"
        ),
    ]

    for video in sample_videos:
        db.add(video)

    db.commit()
    return {"message": "샘플 데이터가 성공적으로 삽입되었습니다!"}