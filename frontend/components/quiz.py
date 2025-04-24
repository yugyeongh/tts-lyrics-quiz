import streamlit as st
import json
from utils.summary_lyrics import summarize_lyrics_with_eeve

def load_songs():
    try:
        with open("../data/songs.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("songs.json 파일을 찾을 수 없습니다.")
        return []
    except json.JSONDecodeError:
        st.error("songs.json 파일 형식이 잘못되었습니다.")
        return []

def render_quiz():
    st.audio(st.session_state.current_audio, format="audio/mp3")
    st.success("✅ 재생 중")

    answer = st.text_input("정답을 입력하세요:", key="answer_input")
    if st.button("정답 제출", key="submit_answer"):
        correct = answer.strip().lower() == st.session_state.current_title.lower()
        st.session_state.answer_status = 'correct' if correct else 'wrong'

        if correct:
            st.success("🎉 정답입니다!")
        else:
            st.error("❌ 틀렸습니다. 다시 시도해보세요!")

        st.rerun()

    if st.button("💡 힌트 보기", key="show_hint"):
        songs = load_songs()  # songs.json 파일에서 데이터를 로드

        if songs:
            # 전체 노래 목록에서 current_title에 해당하는 노래 찾기
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
