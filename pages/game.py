import streamlit as st
from styles.main_styles import main_style
from utils.session import init_session_state
from components.header import render_header
from components.status import render_tts_status
from components.quiz import render_quiz
from utils.tts import generate_tts

st.set_page_config(page_title="AI 가사 낭독 퀴즈", page_icon="🎵", layout="centered")
st.markdown(main_style(), unsafe_allow_html=True)

init_session_state()
render_header()
render_tts_status()

if st.session_state.tts_state == 'loading':
    generate_tts()

if st.button(st.session_state.button_text):
    if st.session_state.remaining_songs:
        st.session_state.tts_state = 'loading'
        st.session_state.answer_status = None
        st.rerun()
    else:
        st.warning("🎉 모든 노래를 다 들었습니다! 페이지를 새로고침해주세요.")
        
if st.session_state.tts_state == 'playing':
    render_quiz()
