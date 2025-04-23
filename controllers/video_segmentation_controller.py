import re
from typing import List
from models.video_segment import VideoSegment
import logging

def time_str_to_seconds(time_str: str) -> int:
    """
    Converts a time string in "MM:SS" format to total seconds as an integer.

    Args:
        time_str (str): Time string, e.g., "02:30"

    Returns:
        int: Total seconds, e.g., 150
    """
    minutes, seconds = map(int, time_str.strip().split(":"))
    return minutes * 60 + seconds

def seconds_to_time_str(seconds: float) -> str:
    """
    Converts seconds into a formatted time string "MM:SS".

    Args:
        seconds (float): Total seconds

    Returns:
        str: Formatted time string, e.g., "02:30"
    """
    minutes = int(seconds) // 60
    remaining_seconds = int(seconds) % 60
    return f"{minutes:02}:{remaining_seconds:02}"

def segment_video_by_description(video_id: str, description: str) -> List[VideoSegment]:
    """
    Parses a video description to extract time-stamped segments and returns a list of VideoSegment objects.

    The description should contain a separator (e.g., "=====") dividing the intro from the time-stamped list,
    and each segment line should begin with a time string and title.

    Args:
        video_id (str): The ID of the video.
        description (str): The full video description, including intro text and segment markers.

    Returns:
        List[VideoSegment]: A list of parsed segments with title, time range, and metadata.
    """
    # Split the description into context and segments
    parts = re.split(r"=+", description)
    description_context = parts[0].strip() if len(parts) > 1 else ""
    segment_lines = parts[1].strip().splitlines() if len(parts) > 1 else description.strip().splitlines()

    # Define regex patterns for time-stamped segments and tags
    segment_pattern = r"(\d{2}:\d{2})\s*[|\-]?\s*(.+)"
    # tag_pattern = r"#(\w+)"

    matches = []
    for line in segment_lines:
        match = re.match(segment_pattern, line)
        if match:
            matches.append((match.group(1), match.group(2).strip()))

    # Extract tags from the description
    # tags = re.findall(tag_pattern, description)

    segments = []
    for idx, (start_str, title) in enumerate(matches):
        start_sec = time_str_to_seconds(start_str)
        end_sec = time_str_to_seconds(matches[idx + 1][0]) if idx + 1 < len(matches) else start_sec + 90.0

        clean_title = title.strip()

        seg = VideoSegment(
            id=f"{video_id}_seg_{idx}",
            video_id=video_id,
            title=clean_title,
            start_time=start_sec,
            tags=[],
            keywords=[],
            end_time=end_sec,
            summary=description_context,
            cognitive_level="Understand",
            dok_level="Level 2"
        )
        segments.append(seg)
        logging.info(f"Segment {idx}: {clean_title} ({seconds_to_time_str(start_sec)} - {seconds_to_time_str(end_sec)})")

    return segments
