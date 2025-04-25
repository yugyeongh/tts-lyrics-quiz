import streamlit as st
from gtts import gTTS
import io
import re

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def generate_tts():
    song = st.session_state.remaining_songs.pop()
    title = sanitize_filename(song['song_title'])
    lyrics = "\n".join(song['lyrics']) if isinstance(song['lyrics'], list) else song['lyrics']

    try:
        tts = gTTS(text=lyrics, lang='ko')
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)

        st.session_state.current_audio = audio_fp
        st.session_state.current_title = title
        st.session_state.tts_state = 'playing'
        st.session_state.button_text = "🎵 다음 노래 듣기"
        st.session_state.question_number += 1
        st.rerun()
    except Exception as e:
        st.error(f"❌ '{title}' 변환 중 오류 발생: {e}")
        st.session_state.tts_state = 'initial'
