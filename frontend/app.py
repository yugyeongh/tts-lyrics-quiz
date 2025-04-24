import streamlit as st
import streamlit.components.v1 as components
from styles import main_style

st.set_page_config(page_title="AI 가사 낭독 퀴즈", page_icon="🎵", layout="centered")
st.markdown(main_style(), unsafe_allow_html=True)

if 'is_loading' not in st.session_state:
    st.session_state.is_loading = False
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False


with st.container():
    st.markdown('<h1 class="title"><span>AI</span> <span>가사</span> <span>낭독 퀴즈</span></h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    
    if st.button("게임 시작하기", key="start", use_container_width=True):
            st.session_state.is_loading = True
            st.switch_page("pages/game.py")
    
    st.markdown('</div>', unsafe_allow_html=True)
