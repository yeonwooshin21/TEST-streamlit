import streamlit as st
from datetime import datetime

# 앱 제목
st.title("YouTube OCR 작업 앱 (테스트)")
st.write("✅ 클라우드 배포 및 비밀번호 인증, 로깅 테스트 페이지입니다.")

# 비밀번호 입력
password = st.text_input("비밀번호를 입력하세요", type="password")

# 접속 시도 시간 기록
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 로그 파일 이름
LOG_FILE = "access_log.txt"

# 비밀번호 검증
if password:
    if password != st.secrets["APP_PASSWORD"]:
        # 실패 로그 기록
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[실패] {now} - 잘못된 비밀번호 입력\n")
        st.error("❌ 비밀번호가 올바르지 않습니다.")
        st.stop()
    else:
        # 성공 로그 기록
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[성공] {now} - 접근 성공\n")
        st.success("✅ 접근 성공! YouTube OCR 테스트 화면을 표시합니다.")
else:
    st.stop()

# --- 여기에부터는 인증 성공 후 표시되는 메인 콘텐츠 ---
st.subheader("🎬 YouTube 영상 테스트 입력")

url = st.text_input("YouTube 영상 링크 입력")
if url:
    st.write(f"입력된 링크: {url}")
