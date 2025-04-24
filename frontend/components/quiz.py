import streamlit as st

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
        if st.session_state.remaining_songs:
            current_lyrics = st.session_state.remaining_songs[-1]["lyrics"]
            hint = current_lyrics[0] if isinstance(current_lyrics, list) else current_lyrics[:20]
            st.info(f"힌트: {hint}")
        else:
            st.info("남은 노래가 없습니다.")
