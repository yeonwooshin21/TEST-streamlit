import cv2
import pytesseract
import numpy as np
from pytube import YouTube
from PIL import Image, ImageFilter, ImageEnhance
import os


def download_video(video_url, output_path="downloads"):
    """YouTube 영상을 다운로드합니다."""
    yt = YouTube(video_url)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    video_path = yt.streams.filter(res="720p").first().download(output_path)
    print(f"Downloaded video to {video_path}")
    return video_path


def extract_frames(video_path, frame_interval=2, output_path="frames"):
    """2초 간격으로 프레임을 추출합니다."""
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    success, frame = video.read()
    count = 0
    frame_count = 0

    while success:
        if int(count % (fps * frame_interval)) == 0:  # frame_interval 초 간격
            frame_filename = os.path.join(output_path, f"frame_{frame_count}.png")
            cv2.imwrite(frame_filename, frame)
            print(f"Saved frame: {frame_filename}")
            frame_count += 1
        success, frame = video.read()
        count += 1
    video.release()
    return output_path


def preprocess_image(image_path):
    """이미지를 전처리합니다."""
    image = Image.open(image_path)
    image = image.convert('L')  # 흑백 처리
    image = image.filter(ImageFilter.MedianFilter())  # 잡음 제거
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # 대비 증가

    # OpenCV로 추가 전처리
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_GRAY2BGR)
    _, image_cv = cv2.threshold(image_cv, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # OTSU 이진화
    image_cv = cv2.resize(image_cv, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

    # Pillow 이미지로 변환
    final_image = Image.fromarray(image_cv)
    return final_image


def extract_text_from_frames(frames_path, lang="kor", config="--psm 6 --oem 3"):
    """추출된 프레임에서 텍스트를 OCR로 추출합니다."""
    texts = []
    for frame_file in sorted(os.listdir(frames_path)):
        if frame_file.endswith(".png"):
            frame_path = os.path.join(frames_path, frame_file)
            processed_image = preprocess_image(frame_path)
            text = pytesseract.image_to_string(processed_image, lang=lang, config=config)
            print(f"Extracted text from {frame_file}:\n{text}\n")
            texts.append(text)
    return texts


if __name__ == "__main__":
    # 1. 유튜브 영상 URL
    video_url = "https://www.youtube.com/watch?v=Q_RmG8Dxvx4"  # 유튜브 영상 URL을 여기에 입력하세요.

    # 2. 영상 다운로드
    video_path = download_video(video_url)

    # 3. 프레임 추출
    frames_dir = extract_frames(video_path, frame_interval=2)

    # 4. 프레임에서 텍스트 추출
    texts = extract_text_from_frames(frames_dir)

    # 5. 텍스트 결과 출력
    print("Final OCR Texts from Frames:")
    for idx, text in enumerate(texts):
        print(f"Frame {idx}:\n{text}")