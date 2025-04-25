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

# 상태에 따라 TTS 상태 UI 렌더링
render_tts_status()

# TTS 재생 준비
if st.session_state.tts_state == 'loading':
    generate_tts()

# 퀴즈 영역
with st.container():
    if st.session_state.tts_state == 'playing':
        render_quiz()

    st.markdown("---")

    # Footer 버튼 (다음 노래 듣기)
    col_spacer, col_button, col_spacer2 = st.columns([1, 2, 1])
    with col_button:
        if st.button(st.session_state.button_text, use_container_width=True):
            if st.session_state.remaining_songs:
                st.session_state.tts_state = 'loading'
                st.session_state.answer_status = None
                st.rerun()
            else:
                st.warning("🎉 모든 노래를 다 들었습니다! 페이지를 새로고침해주세요.")
