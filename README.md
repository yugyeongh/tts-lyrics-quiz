# 🤖 AI 가사 낭독 퀴즈
> AI 음성이 읽어주는 가사의 제목을 맞춰라!

<hr/>

## 💁🏻‍♀️ 게임 소개
- TTS를 활용해 노래 가사를 읽어주는 음성이 재생된다.
- 노래 가사를 듣고 노래의 제목을 맞추면 끝!
<br/><br/>

<hr/>

## 🔩 기술 스택
<p align="center">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white">
    <img src="https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=vscode&logoColor=white">
</p>
<p align="center">
    <img src="https://img.shields.io/badge/streamlit-%23FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white" />
    <img src="https://img.shields.io/badge/RunPod-%23000000.svg?style=for-the-badge&logo=runpod&logoColor=white" />
    <img src="https://img.shields.io/badge/HuggingFace-%23FFD21F.svg?style=for-the-badge&logo=huggingface&logoColor=black" />
</p>
<br/><br/>

<hr/>

## 🗂️ 파일 구조
<pre><code>
    📂 tts-lyrics-quiz/
    │
    ├── 📜 app.py                      ← 🎬 앱 진입점 (Streamlit 실행)
    │   └── 호출: 📁pages/game.py
    │
    ├── 📜 generate_hint.py           ← 💡 EEVE 기반 가사 요약만 실행 시 사용 (백엔드)
    ├── 📜 generate_tts.py            ← 🔊 TTS 파일 생성만 실행 시 사용 (백엔드)
    │
    ├── 📁 pages/
    │   └── 📜 game.py                ← 🎮 게임 페이지 본체
    │       └── import:
    │           ├── components.header.py    ← 타이틀, 설명 렌더링
    │           ├── components.quiz.py      ← 정답 입력, 힌트 버튼, 정답 판정
    │           ├── components.status.py    ← 정답 여부 아이콘 출력
    │           ├── utils.session.py        ← 세션 상태 관리
    │           ├── utils.summary_lyrics.py ← 가사 요약 (EEVE API)
    │           ├── utils.tts.py            ← TTS URL 제공
    │           └── styles.main_styles.py   ← CSS 커스터마이징
    │
    ├── 📁 components/
    │   ├── 📜 header.py             ← ⬆️ 상단 "문제" 타이틀 렌더링
    │   ├── 📜 quiz.py               ← 🧠 퀴즈 입력, 힌트 버튼, 정답 체크
    │   └── 📜 status.py             ← ✅❌ 정답/오답 결과 출력 (아이콘/텍스트)
    │
    ├── 📁 data/
    │   └── 📜 songs.json            ← 🎵 노래 정보 (가사, 제목, TTS 경로 등 저장)
    │
    ├── 📁 styles/
    │   └── 📜 main_styles.py        ← 🎨 전체 스타일 정의 (폰트, 버튼, 색상 등)
    │
    └── 📁 utils/
        ├── 📜 session.py            ← 💾 세션 스토리지 관리
        ├── 📜 summary_lyrics.py     ← ✨ EEVE 요약 호출 (Open API)
        └── 📜 tts.py                ← 🔉 TTS URL 제공 함수
    
</code></pre>

<br/><br/>

<hr/>

## 😄 LLM 모델
- 야놀자의 `EEVE-Korean-10.8B` 모델 사용
  - 적용: 사용자에게 노래 가사의 핵심을 요약하여 힌트 제공

<hr/>

## 🔊 TTS 모델
- Google의 `gTTS (Google Text-to-Speech)` 사용
  - 적용: 노래 가사 텍스트를 한국어 음성으로 변환하여 MP3 파일로 저장

<br/><br/>

<hr/>

## 실행 화면
- main page
<p align="center"> 
    <img src="https://github.com/user-attachments/assets/7a62a05e-ba3e-4e80-84fe-74bb49099572">
</p>
- game page
<p align="center"> 
    <img src="https://github.com/user-attachments/assets/c3189ba8-a92e-495c-9b52-c83d7eb81992">
    <img src="https://github.com/user-attachments/assets/45155be9-1b5f-48a4-b4e3-44a232dd3012">
</p>



