import streamlit as st

def render_tts_status():
    state = st.session_state.tts_state
    status = st.session_state.answer_status

    if state == 'loading':
        st.markdown("""
            <div class="icon-container">
                <div class="loading-icon">
                    <div class="loading-spinner"></div>
                    TTS 변환 중...
                </div>
            </div>
        """, unsafe_allow_html=True)
    elif state == 'playing':
        icon = "정답" if status == 'correct' else "🔊"
        st.markdown(f"""
            <div class="icon-container">
                <div class="speaker-icon-playing">{icon}</div>
            </div>
        """, unsafe_allow_html=True)
