import json
import re
from gtts import gTTS

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

with open('songs.json', 'r', encoding='utf-8') as file:
    songs_data = json.load(file)

# 각 노래에 대해 반복
for song in songs_data:
    title = sanitize_filename(song['song_title'])
    lyrics = song['lyrics']

    if isinstance(lyrics, list):
        input_text = "\n".join(lyrics)
    else:
        input_text = lyrics

    try:
        tts = gTTS(text=input_text, lang='ko')

        filename = f"{title}.mp3"
        tts.save(filename)

        print(f"✅ 음성 파일이 저장되었습니다: {filename}")
    except Exception as e:
        print(f"❌ {title} 저장 중 오류 발생: {e}")
