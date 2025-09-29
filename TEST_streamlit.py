import streamlit as st

st.title("YouTube OCR 작업 앱 (테스트)")
st.write("✅ 클라우드 배포 성공 여부만 확인하는 페이지입니다.")

url = st.text_input("YouTube 영상 링크 입력")
if url:
    st.write(f"입력된 링크: {url}")