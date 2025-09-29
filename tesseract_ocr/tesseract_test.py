import cv2
import pytesseract
import numpy as np
from pytube import YouTube
from PIL import Image, ImageFilter, ImageEnhance

def preprocess_image(image_path):
    # 1. Pillow로 기본 전처리 수행
    image = Image.open(image_path)
    image = image.convert('L')  # 흑백 처리
    image = image.filter(ImageFilter.MedianFilter())  # 잡음 제거
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # 대비 증가

    # 2. OpenCV로 추가 전처리 (이진화 및 크기 조정)
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_GRAY2BGR)  # Pillow 이미지를 OpenCV로 변환
    _, image_cv = cv2.threshold(image_cv, 150, 255, cv2.THRESH_BINARY)  # 이진화
    image_cv = cv2.resize(image_cv, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)  # 크기 조정
    
    # 3. 다시 Pillow 이미지로 변환 후 저장
    final_image = Image.fromarray(image_cv)
    final_image.save("preprocessed_image.png")
    return final_image

# 전처리된 이미지로 OCR 실행
image_path = "/Users/shin-yeon-woo/Desktop/tale_project/tesseract_ocr/test.png"
processed_image = preprocess_image(image_path)

# Tesseract OCR 실행 (config 옵션 추가)
# config에 PSM 설정 및 필요시 추가 옵션 설정 가능
config = '--psm 6 --oem 3'  # PSM 6: 한 줄 텍스트로 간주, OEM 3: 최신 OCR 엔진 사용
text = pytesseract.image_to_string(processed_image, lang='kor', config=config)

print("인식된 텍스트:")
print(text)
