import streamlit as st
import json
import random

def init_session_state():
    defaults = {
        'tts_state': 'initial',
        'current_audio': None,
        'current_title': None,
        'question_number': 1,
        'button_text': "🎵 노래 듣기",
        'answer_status': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if 'remaining_songs' not in st.session_state:
        with open('data/songs.json', 'r', encoding='utf-8') as f:
            songs = json.load(f)
            random.shuffle(songs)
            st.session_state.remaining_songs = songs
