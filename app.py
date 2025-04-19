from controllers.youtube_extractor import YouTubeExtractor
from controllers.youtube_transfomer import YouTubeTransformer
from controllers.youtube_loader import YouTubeLoader  
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 불러오기

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# YTN사이언스 채널명: UCZdBJIbJz0P9xyFipgOj1fA
# YTN사이언스 채널로부터 PLAYLIST와 관련된 비디오를 모두 수집 
extractor = YouTubeExtractor(api_key=YOUTUBE_API_KEY)
channel  = extractor.extract_all(channel_id="UCZdBJIbJz0P9xyFipgOj1fA")


# 수집된 파일을 파일로 출력
loader = YouTubeLoader()
loader.save_channel_to_csv(channel, "channel_videos.csv")

print(channel.title)
print(f"총 재생목록 수: {len(channel.playlists)}")
print(f"첫 번째 비디오 제목: {channel.playlists[0].videos[0].title}")

total_videos = sum(len(playlist.videos) for playlist in channel.playlists)
print(f"총 비디오 수: {total_videos}")