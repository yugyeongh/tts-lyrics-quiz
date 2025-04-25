import json
from utils.summary_lyrics import summarize_lyrics_with_eeve

def generate_hints_for_songs():
    with open("data/songs.json", "r", encoding="utf-8") as file:
        songs = json.load(file)

    for song in songs:
        lyrics = song.get("lyrics", "")
        if lyrics:
            print(f"Generating hint for: {song['song_title']}")
            song["hint"] = summarize_lyrics_with_eeve(lyrics)
        else:
            song["hint"] = ""

    with open("data/songs.json", "w", encoding="utf-8") as file:
        json.dump(songs, file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generate_hints_for_songs()
