import streamlit as st
import json
import re
import random
import io
import threading
import queue
from gtts import gTTS
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import speech_recognition as sr
import av

# 스타일 설정 (원하는 CSS 스타일 여기에 넣어도 됨)
MAIN_STYLES = """
<style>
.question-number {
    font-size: 30px;
    font-weight: bold;
    text-align: center;
}
.icon-container {
    text-align: center;
    margin-top: 20px;
}
.loading-icon {
    font-size: 18px;
    color: gray;
}
.speaker-icon-playing {
    font-size: 40px;
    color: green;
}
</style>
"""

# 페이지 설정
st.set_page_config(
    page_title="AI 가사 낭독 퀴즈 - 게임",
    page_icon="🎵",
    layout="centered"
)

st.markdown(MAIN_STYLES, unsafe_allow_html=True)

# 특수문자 제거
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

# 상태 초기화
if 'remaining_songs' not in st.session_state:
    with open('./data/songs.json', 'r', encoding='utf-8') as file:
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
if 'answer_result' not in st.session_state:
    st.session_state.answer_result = ''

# 문제 번호 표시
st.markdown(f'''
    <h1 class="question-number">
        <span class="number">{st.session_state.question_number}</span><span class="word">번</span> <span class="question">문제</span>
    </h1>
''', unsafe_allow_html=True)

# 상태별 표시
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
    icon = "🔊" if "정답" not in st.session_state.answer_result else st.session_state.answer_result
    st.markdown(f'''
        <div class="icon-container">
            <div class="speaker-icon-playing">{icon}</div>
        </div>
    ''', unsafe_allow_html=True)

# 버튼 → TTS 시작
if st.button(st.session_state.button_text):
    if st.session_state.remaining_songs:
        st.session_state.tts_state = 'loading'
        st.rerun()
    else:
        st.warning("🎉 모든 노래를 다 들었습니다! 페이지를 새로고침해주세요.")

# TTS 변환
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
        st.session_state.answer_result = ''
        st.rerun()
    except Exception as e:
        st.error(f"❌ {title} 변환 중 오류 발생: {e}")
        st.session_state.tts_state = 'initial'

# STT용 큐와 쓰레드
audio_queue = queue.Queue()
recognizer = sr.Recognizer()

class AudioProcessor:
    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        pcm = frame.to_ndarray().flatten().astype("int16").tobytes()
        audio_queue.put(pcm)
        return frame

def recognize_from_mic():
    audio_data = b""
    in_answer_mode = False

    while True:
        try:
            pcm = audio_queue.get(timeout=3)
            audio_data += pcm
            if len(audio_data) > 16000 * 4:
                with sr.AudioData(audio_data, 16000, 2) as audio:
                    try:
                        text = recognizer.recognize_google(audio, language="ko-KR").lower()
                        print("🎤 인식 결과:", text)

                        if "정답" in text:
                            st.session_state.answer_result = "🎤 정답 모드: 정답을 말해주세요!"
                            in_answer_mode = True
                        elif in_answer_mode:
                            if st.session_state.current_title.lower() in text:
                                st.session_state.answer_result = "정답입니다🤩"
                            else:
                                st.session_state.answer_result = "오답입니다🚨"
                            in_answer_mode = False
                    except:
                        pass
                audio_data = b""
        except queue.Empty:
            continue

# 백그라운드 STT 쓰레드 실행
threading.Thread(target=recognize_from_mic, daemon=True).start()

# webrtc 시작
webrtc_streamer(
    key="stt",
    mode=WebRtcMode.SENDONLY,
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True, "video": False},
    async_processing=True,
)

# TTS 재생
if st.session_state.tts_state == 'playing':
    st.audio(st.session_state.current_audio, format="audio/mp3")
    st.markdown("🎙️ 마이크가 켜져 있습니다. '정답'을 말하면 정답을 외칠 수 있어요!")
    if st.session_state.answer_result:
        st.markdown(f"## {st.session_state.answer_result}")

