def main_style():
    styles = """
    <style>
    @import url('https://cdn.jsdelivr.net/gh/ungveloper/web-fonts/GmarketSans/font-face.css');
    @import url('https://cdn.jsdelivr.net/gh/ungveloper/web-fonts/GmarketSans/font-family.css');

    /* Hide scrollbar for all elements */
    ::-webkit-scrollbar {
        display: none !important;
    }
    
    /* Hide scrollbar for Firefox */
    * {
        scrollbar-width: none !important;
    }
    
    /* Hide scrollbar for IE and Edge */
    * {
        -ms-overflow-style: none !important;
    }

    /* Override Streamlit's default styles */
    .stApp {
        background: linear-gradient(
            45deg,
            #8B4513,
            #654321,
            #8B4513,
            #654321
        ) !important;
        background-size: 400% 400% !important;
        margin: 0 !important;
        padding: 2rem !important;
        min-height: 100vh;
        box-sizing: border-box;
        border: 60px solid #D4BEA2;
        border-radius: 25px;
        position: relative;
    }

    .stApp::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.5' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100' height='100' filter='url(%23noise)' opacity='0.08'/%3E%3C/svg%3E");
        opacity: 0.1;
        pointer-events: none;
    }

    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: calc(100vh - 4rem);
        position: relative;
        z-index: 1;
    }

    /* Hide Streamlit elements */
    header, footer, #MainMenu {
        display: none !important;
    }

    /* Hide sidebar */
    section[data-testid="stSidebar"] {
        display: none !important;
    }

    /* Title style */
    .title {
        font-family: 'GmarketSans', sans-serif !important;
        font-size: 150px !important;
        font-weight: 900 !important;
        text-align: center;
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, calc(-50% - 100px));
        white-space: nowrap;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }

    .title span:nth-child(1) {
        color: #FF8A00;
        -webkit-text-stroke: 5px #000;
    }
    .title span:nth-child(2) {
        color: #40E0D0;
        -webkit-text-stroke: 5px #000;
    }
    .title span:nth-child(3) {
        color: #FFD700;
        -webkit-text-stroke: 5px #000;
    }

    /* Button container */
    .button-container {
        margin-top: 50px !important;
        display: flex !important;
        justify-content: center !important;
        width: 140px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    /* Button style */
    .stButton {
        margin: 0 !important;
        width: 100% !important;
    }

    .stButton > button {
        width: 100% !important;
        height: 100px !important;
        border-radius: 15px !important;
        font-size: 50px !important;
        font-family: 'GmarketSans', sans-serif !important;
        font-weight: 900 !important;
        background: white;
        color: black;
        border: 5px solid #FFD700 !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 10px 0 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        letter-spacing: 0.1em !important;
    }

    .stButton > button:hover {
        background: #FFD700 !important;
        color: #8B4513 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3) !important;
    }

    /* Additional container adjustments */
    div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }
    </style>
""" 
    return styles