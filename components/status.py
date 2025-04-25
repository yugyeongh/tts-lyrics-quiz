import streamlit as st

def render_tts_status():
    state = st.session_state.tts_state
    status = st.session_state.answer_status

    if state == 'loading':
        st.markdown("""
            <div class="icon-container">
                <div class="loading-icon">
                    <div class="loading-spinner"></div>
                    노래 불러오는 중...
                </div>
            </div>
        """, unsafe_allow_html=True)
    # elif state == 'playing':
    #     icon = "정답" if status == 'correct' else "🔊"
    #     st.markdown(f"""
    #         <div class="icon-container">
    #             <div class="speaker-icon-playing">{icon}</div>
    #         </div>
    #         <style>
    #             .speaker-icon-playing {{
    #                 font-size: 200px; /* 원하는 크기로 조정 */
    #             }}
    #         </style>
    #     """, unsafe_allow_html=True)
