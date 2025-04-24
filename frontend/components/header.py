import streamlit as st

def render_header():
    st.markdown(f"""
        <h1 class="question-number">
            <span class="number">{st.session_state.question_number}</span>
            <span class="word">번</span> 
            <span class="question">문제</span>
        </h1>
    """, unsafe_allow_html=True)
