import json
import re
from gtts import gTTS

# 파일 이름으로 사용할 수 없는 문자 제거 함수
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

# songs.json 파일 열기
with open('songs.json', 'r', encoding='utf-8') as file:
    songs_data = json.load(file)

# 각 노래에 대해 반복
for song in songs_data:
    title = sanitize_filename(song['song_title'])  # 파일명 안전하게 만들기
    lyrics = song['lyrics']

    # lyrics가 리스트이면 하나의 문자열로 합치기
    if isinstance(lyrics, list):
        input_text = "\n".join(lyrics)
    else:
        input_text = lyrics

    try:
        # 텍스트 음성 변환
        tts = gTTS(text=input_text, lang='ko')

        # 파일 이름으로 저장
        filename = f"{title}.mp3"
        tts.save(filename)

        print(f"✅ 음성 파일이 저장되었습니다: {filename}")
    except Exception as e:
        print(f"❌ {title} 저장 중 오류 발생: {e}")
