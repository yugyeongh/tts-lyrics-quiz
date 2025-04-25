import streamlit as st
import json
from utils.summary_lyrics import summarize_lyrics_with_eeve

def load_songs():
    try:
        with open("data/songs.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("songs.json 파일을 찾을 수 없습니다.")
        return []
    except json.JSONDecodeError:
        st.error("songs.json 파일 형식이 잘못되었습니다.")
        return []

def render_quiz():
    st.markdown(f"""
            <div class="icon-container">
                <div class="speaker-icon-playing">🔊</div>
            </div>
            <style>
                .speaker-icon-playing {{
                    font-size: 200px;
                    text-align: center;
                }}
            </style>
        """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.5, 3, 2])

    with col1:
        if st.session_state.current_audio:
            st.audio(st.session_state.current_audio, format='audio/mp3')

    with col2:
        if st.button("💡 힌트 보기", key="show_hint"):
            songs = load_songs()

            if songs:
                current_lyrics = None
                for song in songs:
                    if song["song_title"] == st.session_state.current_title:
                        current_lyrics = song.get("lyrics", "")
                        break

                if current_lyrics:
                    with st.spinner("힌트 생성 중..."):
                        hint = summarize_lyrics_with_eeve(current_lyrics)
                        st.markdown(
                            f"""
                            <div style="background-color: white; padding: 10px; border-radius: 5px; border: 2px solid #FF8A00; margin-top: 20px;">
                                <span style="color: black; font-size: 18px;">💡 힌트: {hint}</span>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.warning("현재 노래를 찾을 수 없거나 가사가 없습니다.")
            else:
                st.warning("노래 목록을 불러올 수 없습니다.")

    with col3:
        st.markdown(
        """
        <style>
            .stTextInput label {
                font-family: 'Gmarket Sans', sans-serif;
                font-size: 22px; 
                color: white; 
            }
            .stTextInput>div>div>input {
                font-family: 'Gmarket Sans', sans-serif;
                font-size: 18px;
                color: black;
                background-color: white;
                border: 2px solid white;
                padding: 10px;
                border-radius: 5px;
            }
            .stButton>button {
                margin-top: 20px;
            }
            /* 힌트 보기 버튼 스타일 */
            .stButton>button:nth-child(1) {
                border: 2px solid #FF8A00;
                background-color: white;
                color: #FF8A00;
            }
            .stButton>button:nth-child(1):hover {
                background-color: #FF8A00;
                color: white;
            }
            /* 제출 버튼 스타일 */
            .stButton>button:nth-child(2) {
                border: 2px solid orange;
                background-color: white;
                color: #40E0D0;
            }
            .stButton>button:nth-child(2):hover {
                background-color: #40E0D0;
                color: white;
            }
        </style>
        """, unsafe_allow_html=True)

        answer = st.text_input("🎤 정답을 입력하세요:", key="answer_input")
        if st.button("제출"):
            if answer.strip() == st.session_state.current_title:
                st.markdown(
            """
            <style>
                .success-msg {
                    background-color: #d4edda; /* 연두색 배경 */
                    color: #155724; /* 검색 글씨 (어두운 녹색) */
                    padding: 10px;
                    border-radius: 5px;
                    font-size: 16px;
                    font-weight: bold;
                    margin-top: 10px;
                }
            </style>
            <div class="success-msg">🎉 정답입니다!</div>
            """, unsafe_allow_html=True)
                st.session_state.answer_status = "correct"
            else:
                st.markdown(
            """
            <style>
                .error-msg {
                    background-color: #f8d7da; /* 분홍색 배경 */
                    color: #721c24; /* 검정 글씨 */
                    padding: 10px;
                    border-radius: 5px;
                    font-size: 16px;
                    font-weight: bold;
                    margin-top: 10px;
                }
            </style>
            <div class="error-msg">❌ 오답입니다.</div>
            """, unsafe_allow_html=True)
                st.session_state.answer_status = "incorrect"
