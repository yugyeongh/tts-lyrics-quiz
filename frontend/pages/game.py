import streamlit as st
import json
import re
import random
import io
from gtts import gTTS
from styles import MAIN_STYLES  # 스타일 파일을 별도로 사용 중이라면 필요

# 페이지 설정
st.set_page_config(
    page_title="AI 가사 낭독 퀴즈 - 게임",
    page_icon="🎵",
    layout="centered"
)

# CSS 스타일 적용
st.markdown(MAIN_STYLES, unsafe_allow_html=True)

# 특수문자 제거 (파일 이름 등)
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

# 상태 초기화
if 'remaining_songs' not in st.session_state:
    with open('../data/songs.json', 'r', encoding='utf-8') as file:
        st.session_state.remaining_songs = json.load(file)
        random.shuffle(st.session_state.remaining_songs)

if 'tts_state' not in st.session_state:
    st.session_state.tts_state = 'initial'
if 'current_audio' not in st.session_state:
    st.session_state.current_audio = None
if 'current_title' not in st.session_state:
    st.session_state.current_title = None
if 'question_number' not in st.session_state:
    st.session_state.question_number = 1
if 'button_text' not in st.session_state:
    st.session_state.button_text = "🎵 노래 듣기"

# 문제 번호 표시
st.markdown(f'''
    <h1 class="question-number">
        <span class="number">{st.session_state.question_number}</span><span class="word">번</span> <span class="question">문제</span>
    </h1>
''', unsafe_allow_html=True)

# 상태에 따라 아이콘 표시
if st.session_state.tts_state == 'loading':
    st.markdown('''
        <div class="icon-container">
            <div class="loading-icon">
                <div class="loading-spinner"></div>
                TTS 변환 중...
            </div>
        </div>
    ''', unsafe_allow_html=True)
elif st.session_state.tts_state == 'playing':
    st.markdown('''
        <div class="icon-container">
            <div class="speaker-icon-playing">🔊</div>
        </div>
    ''', unsafe_allow_html=True)

# 버튼 클릭 → TTS 변환 시작
if st.button(st.session_state.button_text):
    if st.session_state.remaining_songs:
        st.session_state.tts_state = 'loading'
        st.rerun()
    else:
        st.warning("🎉 모든 노래를 다 들었습니다! 페이지를 새로고침해주세요.")
    
    

# 로딩 상태에서 TTS 변환 수행
if st.session_state.tts_state == 'loading':
    song = st.session_state.remaining_songs.pop()
    title = sanitize_filename(song['song_title'])
    lyrics = song['lyrics']
    input_text = "\n".join(lyrics) if isinstance(lyrics, list) else lyrics

    try:
        tts = gTTS(text=input_text, lang='ko')
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)

        st.session_state.current_audio = audio_fp
        st.session_state.current_title = title
        st.session_state.tts_state = 'playing'
        st.session_state.button_text = "🎵 다음 노래 듣기"
        st.rerun()  # 변환 완료 후 다시 실행 (자동 재생 위해)
    except Exception as e:
        st.error(f"❌ {title} 변환 중 오류 발생: {e}")
        st.session_state.tts_state = 'initial'

# 재생 상태에서 오디오 출력
if st.session_state.tts_state == 'playing':
    st.audio(st.session_state.current_audio, format="audio/mp3")
    st.success(f"✅ 재생 중")