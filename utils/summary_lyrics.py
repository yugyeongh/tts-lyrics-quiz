import ollama

def summarize_lyrics_with_eeve(lyrics):
    lyrics_text = lyrics if isinstance(lyrics, str) else " ".join(lyrics)
    prompt = f"노래 가사의 내용을 한 문장으로 요약해줘:\n\n{lyrics_text}"
    
    response = ollama.chat(
        model='EEVE-Korean-10.8B',
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response['message']['content'].strip()