# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite 데이터베이스 경로 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# DB 엔진 생성 (SQLite는 connect_args 필요)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 세션 로컬 객체 (DB 세션 연결용)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모든 모델(Base 클래스)들이 상속받는 기본 클래스
Base = declarative_base()


# 의존성 주입용 함수 — FastAPI 라우트에서 사용
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
