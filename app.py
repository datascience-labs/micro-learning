from controllers.youtube_extractor import YouTubeExtractor
from controllers.youtube_transfomer import YouTubeTransformer
from controllers.youtube_loader import YouTubeLoader  
import os
from dotenv import load_dotenv
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()  # .env 파일 불러오기

logging.info("YouTube API 키 로드 중...")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

logging.info("YouTubeExtractor 초기화 중...")
extractor = YouTubeExtractor(api_key=YOUTUBE_API_KEY)

logging.info("채널 데이터 추출 중...")
channel  = extractor.extract_all(channel_id="UCZdBJIbJz0P9xyFipgOj1fA")

logging.info("채널 데이터 변환 중...")
transfomer = YouTubeTransformer()
transformed_channel = transfomer.transform_channel_videos(channel)

logging.info("채널 데이터를 CSV 파일로 저장 중...")
loader = YouTubeLoader()
loader.save_channel_to_csv(transformed_channel, "channel_videos.csv")

logging.info("채널 정보 출력 중...")
print(channel.title)
print(f"총 재생목록 수: {len(channel.playlists)}")
print(f"첫 번째 비디오 제목: {channel.playlists[0].videos[0].title}")

total_videos = sum(len(playlist.videos) for playlist in channel.playlists)
print(f"총 비디오 수: {total_videos}")

# 세그먼트가 있는 비디오 수 계산 및 출력
videos_with_segments = sum(1 for playlist in channel.playlists for video in playlist.videos if video.segments)
print(f"세그먼트가 있는 비디오 수: {videos_with_segments}")