import streamlit as st

def render_header():
    st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Gmarket+Sans:wght@300;400;500;700&display=swap');
        </style>
        <h2 style='
            text-align: center;
            margin-top: -160px;
            color: white;
            font-size: 60px;
            font-family: "GmarketSans", sans-serif;  /* 지마켓 산스 폰트 적용 */
            text-shadow:
                -2px -2px 0 black,
                 2px -2px 0 black,
                -2px  2px 0 black,
                 2px  2px 0 black;
        '>
            문제
        </h2>
        """, unsafe_allow_html=True)
