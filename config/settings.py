import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 불러오기

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
