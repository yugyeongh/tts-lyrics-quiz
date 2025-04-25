import streamlit as st

def render_header():
    st.markdown(f"<h2 style='text-align: center; font-color: white'>문제 {st.session_state.question_number}번</h2>", unsafe_allow_html=True)
