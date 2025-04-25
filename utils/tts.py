import streamlit as st
import os
import io
import re

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def generate_tts():
    song = st.session_state.remaining_songs.pop()
    title = sanitize_filename(song['song_title'])

    mp3_path = os.path.join("data", "tts", f"{title}.mp3")

    if not os.path.exists(mp3_path):
        st.error(f"❌ '{title}.mp3' 파일이 존재하지 않습니다. 먼저 TTS 파일을 생성해주세요.")
        st.session_state.tts_state = 'initial'
        return

    try:
        with open(mp3_path, "rb") as f:
            audio_bytes = f.read()
            audio_fp = io.BytesIO(audio_bytes)
            audio_fp.seek(0)

        st.session_state.current_audio = audio_fp
        st.session_state.current_title = title
        st.session_state.tts_state = 'playing'
        st.session_state.button_text = "🎵 다음 노래 듣기"
        st.session_state.question_number += 1
        st.rerun()
    except Exception as e:
        st.error(f"❌ '{title}.mp3' 로딩 중 오류 발생: {e}")
        st.session_state.tts_state = 'initial'
