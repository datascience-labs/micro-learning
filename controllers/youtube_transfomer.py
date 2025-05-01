from typing import Dict, List
from models import Playlist, PlaylistMetadata, Video  
from datetime import datetime
from controllers.video_segmentation_controller import segment_video_by_description
from models.channel import Channel
from transformers import pipeline
import youtube_transcript_api
from youtube_transcript_api import YouTubeTranscriptApi

import re
import logging

from models.video_segment import VideoSegment

class YouTubeTransformer:
    def transform_channel_videos(self, channel: Channel):
        """
        채널 객체 내 비디오를 분석하여 세그먼트를 생성하고 태그를 추가합니다.

        Args:
            channel (Channel): 분석할 채널 객체

        Returns:
            Channel: 세그먼트가 추가된 채널 객체
        """
        for playlist in channel.playlists:
            for video in playlist.videos:
                try:
                    # 비디오 설명에서 세그먼트 분리
                    segments = segment_video_by_description(video.id, video.description)
                    if segments:
                        logging.info(f"생성된 세그먼트: {len(segments)}개")
                        logging.info(f"{video.title}의 세그먼트에 자막 추가 중...")
                        video.segments = self.add_subtitles_to_segments(video_id=video.id, segments=segments)

                    extract_subtitles = self.extract_subtitles(video.id)
                    extract_summary = self.generate_summary(extract_subtitles)

                    # 태그 추출 및 추가
                    tag_pattern = r"#(\w+)"
                    tags = re.findall(tag_pattern, video.description)

                    if tags:
                        logging.info(f"추출된 태그: {tags}")

                    # 비디오 객체에 세그먼트 추가
                    video.segments = segments
                    video.tags = tags
                    video.subtitles = extract_subtitles
                    video.summary = extract_summary

                except ValueError as e:
                    print(f"⚠️ {video.title}에서 세그먼트를 생성할 수 없습니다: {e}")

        return channel

    def extract_subtitles(self, video_id: str) -> str:
        """
        비디오 ID를 사용하여 전체 자막을 추출합니다.

        Args:
            video_id (str): 비디오 ID

        Returns:
            str: 추출된 자막 텍스트
        """
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            subtitles = " ".join([entry['text'] for entry in transcript])
            return subtitles
        except youtube_transcript_api._errors.TranscriptsDisabled:
            return "자막이 비활성화된 비디오입니다."
        except youtube_transcript_api._errors.VideoUnavailable:
            return "비디오를 사용할 수 없습니다."
        except Exception as e:
            return f"자막 추출 중 오류 발생: {str(e)}"

    def generate_summary(self, text: str) -> str:
        """
        주어진 텍스트를 요약합니다.

        Args:
            text (str): 요약할 텍스트

        Returns:
            str: 요약된 텍스트
        """
        try:
            summarizer = pipeline(
                "summarization",
                model="lcw99/kobart-summarization",  # 한국어 요약 모델
                tokenizer="lcw99/kobart-summarization",
                device=0 #GPU
            )
            summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
            return summary[0]['summary_text']
        except ImportError:
            return "요약 생성에 필요한 라이브러리가 설치되어 있지 않습니다."
        except Exception as e:
            return f"요약 생성 중 오류 발생: {str(e)}"

    def generate_title(self, text: str) -> str:
        """
        주어진 텍스트를 기반으로 제목을 생성합니다.

        Args:
            text (str): 제목을 생성할 텍스트

        Returns:
            str: 생성된 제목
        """
        # TODO: 제목 생성 로직 구현 (예: OpenAI API 또는 Hugging Face 모델 활용)
        return "생성된 제목"

    def add_subtitles_to_segments(self, video_id: str, segments: List[VideoSegment]):
        """
        각 세그먼트의 시작 시간과 종료 시간에 맞는 자막을 추출하여 추가합니다.

        Args:
            video_id (str): 비디오 ID
            segments (List[VideoSegment]): 세그먼트 리스트

        Returns:
            List[VideoSegment]: 자막이 추가된 세그먼트 리스트
        """
        for segment in segments:
            subtitles = self.extract_subtitles_with_timestamps(
                video_id=video_id,
                start_sec=segment.start_time,
                end_sec=segment.end_time
            )
            segment.summary = self.generate_summary(subtitles)
            segment.subtitles = subtitles

        return segments

    def extract_subtitles_with_timestamps(self, video_id: str, start_sec: float, end_sec: float) -> str:
        """
        비디오 ID와 시간 범위를 사용하여 해당 구간의 자막을 추출합니다.

        Args:
            video_id (str): 비디오 ID
            start_sec (float): 시작 시간 (초 단위)
            end_sec (float): 종료 시간 (초 단위)

        Returns:
            str: 추출된 자막 텍스트
        """
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            subtitles = []

            for entry in transcript:
                if start_sec <= entry['start'] < end_sec:
                    subtitles.append(entry['text'])

            return " ".join(subtitles)
        except youtube_transcript_api._errors.TranscriptsDisabled:
            return "자막이 비활성화된 비디오입니다."
        except youtube_transcript_api._errors.VideoUnavailable:
            return "비디오를 사용할 수 없습니다."
        except Exception as e:
            return f"자막 추출 중 오류 발생: {str(e)}"
