import whisper

def extract_text_from_mp3(mp3_path):
    print("[…] Whisper 모델 로딩 중...")
    model = whisper.load_model("base")
    result = model.transcribe(mp3_path, language='ko')
    text = result['text'].strip()
    return text

def save_metadata(wav_id, text, metadata_path):
    with open(metadata_path, 'w', encoding='utf-8') as f:
        f.write(f"{wav_id}|{text}|{text}\n")
    print(f"[✔] Whisper 텍스트 추출 및 metadata.csv 생성 완료")

if __name__ == "__main__":
    mp3_path = 'data/youtube_output.mp3'
    wav_id = '00001'
    metadata_path = 'data/metadata.csv'

    text = extract_text_from_mp3(mp3_path)

    save_metadata(wav_id, text, metadata_path)
    print(f"[🗣️] 추출된 텍스트: {text}")