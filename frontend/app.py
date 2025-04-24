import streamlit as st
from styles.main_styles import main_style

st.set_page_config(page_title="AI 가사 낭독 퀴즈", page_icon="🎵", layout="centered")
st.markdown(main_style(), unsafe_allow_html=True)

if 'is_loading' not in st.session_state:
    st.session_state.is_loading = False
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False
if 'question_number' not in st.session_state:
    st.session_state.question_number = 1

with st.container():
    st.markdown("""
    <div class="main">
        <h1 class="title">
            <span>AI</span> <span>가사</span> <span>낭독 퀴즈</span>
        </h1>
        <div class="button-container">
    """, unsafe_allow_html=True)

    col1 = st.columns(1)[0]
    
    with col1:
        if st.button("게임 시작하기", key="start", use_container_width=True):
            st.session_state.is_loading = True
            st.switch_page("pages/game.py")
  

    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)
