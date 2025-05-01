import streamlit as st
import pandas as pd

# ✅ 목표 주제 세트
TARGET_TOPICS = {"for loop", "if", "function"}

# ✅ 초기 세션 상태 설정
if 'playlist' not in st.session_state:
    st.session_state.playlist = []
if 'last_added' not in st.session_state:
    st.session_state.last_added = None

st.set_page_config(page_title="Microlearning Playlist Builder", layout="wide")
st.title("🎯 Microlearning Playlist Builder")

# ✅ Dummy 검색 결과 (실제 API로 교체 가능)
dummy_results = [
    {"videoId": "abc123", "title": "Python For Loops", "thumbnailUrl": "https://via.placeholder.com/150", "topics": ["for loop"]},
    {"videoId": "def456", "title": "If Statements", "thumbnailUrl": "https://via.placeholder.com/150", "topics": ["if"]},
    {"videoId": "ghi789", "title": "Python Functions", "thumbnailUrl": "https://via.placeholder.com/150", "topics": ["function"]},
]

# ✅ 추천 영상 mock
related_videos = {
    "abc123": [
        {"videoId": "rel1", "title": "For Loops Advanced", "thumbnailUrl": "https://via.placeholder.com/150", "topics": ["for loop"]},
        {"videoId": "rel2", "title": "Nested For Loops", "thumbnailUrl": "https://via.placeholder.com/150", "topics": ["for loop"]}
    ],
    "def456": [
        {"videoId": "rel3", "title": "If Else Conditions", "thumbnailUrl": "https://via.placeholder.com/150", "topics": ["if"]}
    ],
    "ghi789": [
        {"videoId": "rel4", "title": "Lambda Functions", "thumbnailUrl": "https://via.placeholder.com/150", "topics": ["function"]}
    ]
}

# ✅ Coverage 계산 함수
def calculate_coverage(playlist, target_topics):
    playlist_topics = set()
    for video in playlist:
        playlist_topics.update(video.get('topics', []))
    covered = playlist_topics.intersection(target_topics)
    coverage_ratio = len(covered) / len(target_topics) if target_topics else 1.0
    missing_topics = target_topics - covered
    return coverage_ratio, missing_topics

# ✅ 탭 UI
tab1, tab2 = st.tabs(["🔍 검색", "📚 Playlist 관리"])

# ──────────────── 검색 탭 ────────────────
with tab1:
    st.header("검색")
    keyword = st.text_input("검색어 입력:")
    if st.button("검색"):
        st.subheader("검색 결과")
        for result in dummy_results:
            cols = st.columns([1, 3, 1])
            cols[0].image(result["thumbnailUrl"])
            cols[1].markdown(f"**{result['title']}**\nTopics: {', '.join(result['topics'])}")
            if cols[2].button("Playlist에 추가", key=result["videoId"]):
                st.session_state.playlist.append(result)
                st.session_state.last_added = result["videoId"]

# ──────────────── Playlist 관리 탭 ────────────────
with tab2:
    st.header("나의 Playlist")
    if st.session_state.playlist:
        for idx, video in enumerate(st.session_state.playlist):
            st.markdown(f"{idx+1}. **{video['title']}** (Topics: {', '.join(video.get('topics', []))})")
        
        # ✅ Coverage 계산
        coverage, missing_topics = calculate_coverage(st.session_state.playlist, TARGET_TOPICS)
        st.metric("Coverage", f"{coverage*100:.1f}%")
        
        if missing_topics:
            st.warning(f"부족한 주제: {', '.join(missing_topics)}")
        
        # ✅ 추천 영상 (추가된 마지막 비디오 기준)
        if st.session_state.last_added:
            st.subheader("추천 영상 (비슷한 주제 기반)")
            recs = related_videos.get(st.session_state.last_added, [])
            for rec in recs:
                cols = st.columns([1, 3, 1])
                cols[0].image(rec["thumbnailUrl"])
                cols[1].markdown(f"**{rec['title']}**\nTopics: {', '.join(rec['topics'])}")
                if cols[2].button(f"추천 추가 {rec['videoId']}", key=rec["videoId"]):
                    st.session_state.playlist.append(rec)

        # ✅ CSV 다운로드
        df = pd.DataFrame(st.session_state.playlist)
        csv_data = df.to_csv(index=False)
        st.download_button("Playlist CSV 다운로드", data=csv_data, file_name="playlist.csv", mime="text/csv")

    else:
        st.info("Playlist가 비어있습니다.")

