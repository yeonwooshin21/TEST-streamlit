import os
from googleapiclient.discovery import build
import pandas as pd
import cv2
import pytesseract
from PIL import Image
import numpy as np
from pytube import YouTube
import time

class YouTubeAnalyzer:
    def __init__(self, api_key):
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        
    def get_channel_videos(self, channel_id):
        """채널의 모든 동영상 정보를 가져옵니다."""
        videos = []
        request = self.youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=50,
            type="video",
            order="date"
        )
        
        while request:
            response = request.execute()
            
            for item in response['items']:
                video_id = item['id']['videoId']
                stats = self.youtube.videos().list(
                    part="statistics",
                    id=video_id
                ).execute()
                
                video_data = {
                    'title': item['snippet']['title'],
                    'video_id': video_id,
                    'views': stats['items'][0]['statistics']['viewCount'],
                    'thumbnail': item['snippet']['thumbnails']['high']['url'],
                    'published_at': item['snippet']['publishedAt']
                }
                videos.append(video_data)
            
            request = self.youtube.search().list_next(request, response)
        
        return pd.DataFrame(videos)
    
    def download_and_process_video(self, video_url, output_dir):
        """비디오를 다운로드하고 프레임을 추출합니다."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # 비디오 다운로드
        yt = YouTube(video_url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        video_path = stream.download(output_dir)
        
        # 비디오 프레임 추출
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * 2)  # 2초 간격
        
        frames = []
        frame_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            if frame_count % frame_interval == 0:
                frames.append(frame)
            
            frame_count += 1
            
        cap.release()
        
        # 중복 프레임 제거
        unique_frames = self.remove_duplicate_frames(frames)
        
        return unique_frames
    
    def remove_duplicate_frames(self, frames, threshold=0.95):
        """유사한 프레임을 제거합니다."""
        if not frames:
            return []
            
        unique_frames = [frames[0]]
        
        for frame in frames[1:]:
            is_duplicate = False
            for unique_frame in unique_frames:
                similarity = self.calculate_similarity(frame, unique_frame)
                if similarity > threshold:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_frames.append(frame)
                
        return unique_frames
    
    def calculate_similarity(self, frame1, frame2):
        """두 프레임 간의 유사도를 계산합니다."""
        hist1 = cv2.calcHist([frame1], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([frame2], [0], None, [256], [0, 256])
        
        return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    
    def extract_text_from_frames(self, frames, output_file):
        """프레임에서 텍스트를 추출하고 파일로 저장합니다."""
        texts = []
        
        for i, frame in enumerate(frames):
            # OpenCV BGR을 RGB로 변환
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # PIL Image로 변환
            pil_image = Image.fromarray(rgb_frame)
            # 텍스트 추출
            text = pytesseract.image_to_string(pil_image, lang='kor+eng')
            if text.strip():
                texts.append(f"Frame {i+1}:\n{text}\n")
        
        # 텍스트 파일로 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(texts))

def main():
    # API 키와 채널 ID 설정
    API_KEY = 'YOUR_API_KEY'
    CHANNEL_ID = 'TARGET_CHANNEL_ID'
    OUTPUT_DIR = 'output'
    
    analyzer = YouTubeAnalyzer(API_KEY)
    
    # 1. 채널 영상 정보 수집
    videos_df = analyzer.get_channel_videos(CHANNEL_ID)
    videos_df.to_csv(f'{OUTPUT_DIR}/video_info.csv', index=False)
    
    # 2&3. 각 영상 처리
    for idx, row in videos_df.iterrows():
        video_url = f"https://www.youtube.com/watch?v={row['video_id']}"
        frames = analyzer.download_and_process_video(video_url, f'{OUTPUT_DIR}/videos')
        analyzer.extract_text_from_frames(
            frames, 
            f'{OUTPUT_DIR}/texts/{row["video_id"]}_text.txt'
        )

if __name__ == "__main__":
    main()