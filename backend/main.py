# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- 앱 기본 설정 ---
app = FastAPI(
    title="YouTube OCR Backend",
    description="YouTube 영상 OCR 및 텍스트 관리 백엔드 API",
    version="1.0.0"
)

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
    return {"message": "🚀 FastAPI 서버가 정상적으로 실행되었습니다!"}


# --- 간단한 API 예시 ---
@app.get("/status")
def get_status():
    return {"status": "ok", "detail": "서버가 정상적으로 작동 중입니다."}
