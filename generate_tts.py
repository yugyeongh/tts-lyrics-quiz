import os
import json
import re
from gtts import gTTS

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def generate_tts_for_songs():
    tts_dir = "data/tts"
    os.makedirs(tts_dir, exist_ok=True)

    with open("data/songs.json", "r", encoding="utf-8") as file:
        songs = json.load(file)

    for song in songs:
        title = sanitize_filename(song.get("song_title", "untitled"))
        lyrics = song.get("lyrics", "")
        if isinstance(lyrics, list):
            lyrics = "\n".join(lyrics)

        mp3_path = os.path.join(tts_dir, f"{title}.mp3")

        if not lyrics:
            print(f"❌ No lyrics found for '{title}', skipping.")
            continue

        if os.path.exists(mp3_path):
            print(f"✅ '{title}.mp3' already exists, skipping.")
            continue

        try:
            print(f"🎙️ Generating TTS for: {title}")
            tts = gTTS(text=lyrics, lang='ko')
            tts.save(mp3_path)
        except Exception as e:
            print(f"❌ Error generating TTS for '{title}': {e}")

if __name__ == "__main__":
    generate_tts_for_songs()
