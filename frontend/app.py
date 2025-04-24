import streamlit as st
import streamlit.components.v1 as components
from styles import MAIN_STYLES

# 페이지 설정
st.set_page_config(
    page_title="AI 가사 낭독 퀴즈",
    page_icon="🎵",
    layout="centered"
)

# 세션 상태 초기화
if 'is_loading' not in st.session_state:
    st.session_state.is_loading = False
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False

# CSS 스타일 적용
st.markdown(MAIN_STYLES, unsafe_allow_html=True)

# 메인 컨테이너
with st.container():
    st.markdown('<h1 class="title"><span>AI</span> <span>가사</span> <span>낭독 퀴즈</span></h1>', unsafe_allow_html=True)
    
    # # 상태에 따른 아이콘 표시
    # if st.session_state.is_loading:
    #     st.markdown('<div class="loading-icon">⌛</div>', unsafe_allow_html=True)
    # elif st.session_state.is_playing:
    #     st.markdown('<div class="speaker-icon">🔊</div>', unsafe_allow_html=True)
    
    # 버튼 컨테이너
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    
    # 버튼들을 컬럼으로 나누어 배치
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("게임 시작하기", key="start", use_container_width=True):
            st.session_state.is_loading = True
            # TTS 변환 로직이 여기에 들어갈 예정
            # 변환이 완료되면:
            # st.session_state.is_loading = False
            # st.session_state.is_playing = True
            st.switch_page("pages/game.py")
    
    with col2:
        if st.button("게임 소개", key="info", use_container_width=True):
            st.switch_page("pages/intro.py")
    
    st.markdown('</div>', unsafe_allow_html=True)
