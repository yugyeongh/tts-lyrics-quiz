import streamlit as st

def render_quiz():
    st.audio(st.session_state.current_audio, format="audio/mp3")
    st.success("✅ 재생 중")

    answer = st.text_input("정답을 입력하세요:", key="answer_input")
    if st.button("정답 제출"):
        correct = answer.strip().lower() == st.session_state.current_title.lower()
        st.session_state.answer_status = 'correct' if correct else 'wrong'

        if correct:
            st.success("🎉 정답입니다!")
        else:
            st.error("❌ 틀렸습니다. 다시 시도해보세요!")

        st.rerun()
