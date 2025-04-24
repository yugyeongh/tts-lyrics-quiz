import streamlit as st
import streamlit.components.v1 as components
# from styles import MAIN_STYLES

MAIN_STYLES = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&display=swap');

    /* Hide Streamlit header */
    header {
        display: none !important;
    }

    .main {
        background-color: transparent;
        min-height: 100vh;
        padding: 2rem;
        border: 60px solid #ff4b4b;
        border-radius: 70px;
        box-sizing: border-box;
    }
    .title {
        font-family: 'Black Han Sans', sans-serif;
        font-size: 5.5rem;
        font-weight: 400;
        text-align: center;
        margin: 1.5rem auto;
        padding: 1.5rem 2rem;
        max-width: 1000px;
        line-height: 1.3;
        letter-spacing: -0.02em;
    }
    .title span:nth-child(1) {
        color: #FF8C00;
        -webkit-text-stroke: 4px black;
    }
    .title span:nth-child(2) {
        color: #00CED1;
        -webkit-text-stroke: 4px black;
    }
    .title span:nth-child(3) {
        color: white;
        -webkit-text-stroke: 4px black;
    }

    /* Question Number Style */
    .question-number {
        font-family: 'Black Han Sans', sans-serif;
        font-size: 5.5rem;
        font-weight: 400;
        text-align: center;
        margin: 1.5rem auto;
        padding: 1rem;
        letter-spacing: -0.02em;
        white-space: nowrap;
    }
    .question-number .number {
        color: #FF8C00;
        -webkit-text-stroke: 4px black;
        margin-right: -0.1em;
    }
    .question-number .word {
        color: #00CED1;
        -webkit-text-stroke: 4px black;
    }
    .question-number .question {
        color: white;
        -webkit-text-stroke: 4px black;
        margin-left: 0.2em;
    }

    /* Icon Container */
    .icon-container {
        text-align: center;
        margin: 2rem auto;
        height: 150px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* Loading Icon */
    .loading-icon {
        font-family: 'Black Han Sans', sans-serif;
        font-size: 1.5rem;
        color: #ff4b4b;
    }
    .loading-spinner {
        width: 80px;
        height: 80px;
        margin: 0 auto 1rem;
        border: 8px solid #f3f3f3;
        border-top: 8px solid #ff4b4b;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Playing Speaker Icon */
    .speaker-icon-playing {
        font-size: 8rem;
        animation: pulse 1s ease-in-out infinite;
    }
    @keyframes pulse {
        0% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.2);
        }
        100% {
            transform: scale(1);
        }
    }

    .button-container {
        margin: 3rem auto;
        max-width: 800px;
    }
    /* Style Streamlit columns */
    .css-12w0qpk {
        padding: 0 1rem !important;
    }
    .stButton {
        text-align: center;
    }
    .stButton > button {
        width: 220px !important;
        height: 60px;
        border-radius: 30px;
        font-size: 1.5rem !important;
        font-family: 'Black Han Sans', sans-serif !important;
        font-weight: 400 !important;
        letter-spacing: 0.02em;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
        margin: 0 auto;
    }
    .stButton > button:first-child {
        background: linear-gradient(45deg, #ff4b4b, #ff8f8f);
        color: white;
    }
    .stButton > button:last-child {
        background: linear-gradient(45deg, #4ECDC4, #6BE5D9);
        color: white;
    }
    .stButton > button:first-child:hover {
        background: linear-gradient(45deg, #ff8f8f, #ff4b4b);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    .stButton > button:last-child:hover {
        background: linear-gradient(45deg, #6BE5D9, #4ECDC4);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            120deg,
            transparent,
            rgba(255, 255, 255, 0.3),
            transparent
        );
        transition: 0.5s;
    }
    .stButton > button:hover::before {
        left: 100%;
    }

    /* Hide Streamlit elements */
    #MainMenu {
        display: none !important;
    }
    footer {
        display: none !important;
    }
    </style>
""" 

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
