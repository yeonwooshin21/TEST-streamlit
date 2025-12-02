from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routes import videos, user

# DB 초기화 (테이블 생성)
models.Base.metadata.create_all(bind=engine)

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

@app.get("/")
def read_root():
    return {"message": "Hello World"}