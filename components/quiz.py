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
    col1, col2, col3 = st.columns([1.5, 1, 2])  # 비율 조정 가능

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
                        st.info(f"💡 힌트: {hint}")
                else:
                    st.warning("현재 노래를 찾을 수 없거나 가사가 없습니다.")
            else:
                st.warning("노래 목록을 불러올 수 없습니다.")

    with col3:
        answer = st.text_input("🎤 정답을 입력하세요:", key="answer_input")
        if st.button("제출"):
            if answer.strip() == st.session_state.current_title:
                st.success("🎉 정답입니다!")
                st.session_state.answer_status = "correct"
            else:
                st.error("❌ 오답입니다.")
                st.session_state.answer_status = "incorrect"
