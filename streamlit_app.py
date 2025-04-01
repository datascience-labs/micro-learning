# streamlit_app.py
import streamlit as st
from urllib.parse import urlparse, parse_qs
# from controllers.microlearning_recommender import recommend_sequences_from_segments
from controllers.video_segmentation_controller import segment_video_by_description, seconds_to_time_str
from controllers.youtube_api import fetch_video_details, extract_video_info, fetch_and_parse_youtube_data

st.set_page_config(page_title="MicroLearning Sequence Viewer", layout="wide")
st.title("🧠 MicroLearning Sequence Viewer")

# 유튜브 링크 입력 받기
youtube_url = st.text_input("🎥 Paste a YouTube video link:", value="https://www.youtube.com/watch?v=E6DuimPZDz8&t=7s")

# YouTube 링크에서 Video ID 추출st
def extract_video_id(url):
    try:
        parsed = urlparse(url)
        if parsed.hostname == 'youtu.be':
            return parsed.path[1:]
        elif parsed.hostname in ('www.youtube.com', 'youtube.com'):
            if parsed.path == '/watch':
                return parse_qs(parsed.query)['v'][0]
            elif parsed.path.startswith('/embed/'):
                return parsed.path.split('/')[2]
        return None
    except:
        return None

if youtube_url:
    video_id = extract_video_id(youtube_url)

    if video_id:
        # try:
            with st.spinner("🔍 Fetching video and segmenting..."):
                video_item = fetch_video_details(video_id)
                parsed_data = extract_video_info(video_item)
                channel, video = fetch_and_parse_youtube_data(parsed_data)
                    
                segments = segment_video_by_description(video_id, video.description)
                # st.text(video.description)

            st.video(youtube_url)
            
            st.success(f"✅ {len(segments)} segments found")
            
            if len(segments) > 0:
                for seg in segments:
                    start_param = int(seg.start_time)
                    start_time = seconds_to_time_str(seg.start_time)
                    end_time = seconds_to_time_str(seg.end_time)
                    with st.expander(f"▶️ {seg.title} ( {start_time} - {end_time} ) "):
                        st.markdown(f"**Cognitive Level**: {seg.cognitive_level}")
                        st.markdown(f"**Depth of Knowledge Level**: {seg.dok_level}")
                        st.markdown(f"**Summary**: {seg.summary}")
                        embed_url = f"https://www.youtube.com/embed/{video_id}?start={start_param}&autoplay=1"
                        st.components.v1.iframe(embed_url, height=315)
        # except Exception as e:
            # st.error(f"🚫 Error: {e}")
    else:
        st.warning("❗ Could not extract video ID from URL. Please check the format.")
