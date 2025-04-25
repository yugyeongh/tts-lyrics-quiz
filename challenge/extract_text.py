import subprocess
import os
import whisper
from concurrent.futures import ThreadPoolExecutor

# MP3를 WAV로 변환하고 샘플링 레이트 변경
def mp3_to_wav(mp3_path, wav_path, sample_rate=16000):
    print(f"[🔄] {mp3_path} -> {wav_path} 변환 시작...")
    try:
        # ffmpeg 명령어로 mp3를 wav로 변환 후, 샘플링 레이트 변경
        command = ['ffmpeg', '-i', mp3_path, '-ar', str(sample_rate), wav_path]
        subprocess.run(command, check=True)
        print(f"[✔] 변환 완료: {mp3_path} -> {wav_path} (샘플링 레이트 {sample_rate}Hz)")
    except subprocess.CalledProcessError as e:
        print(f"[❌] 오류 발생: {e}")

# Whisper 모델을 사용하여 텍스트 추출
def extract_text_from_wav(wav_path):
    print(f"[📝] {wav_path}에서 텍스트 추출 시작...")
    model = whisper.load_model("base")
    result = model.transcribe(wav_path, language='ko')
    text = result['text'].strip()
    return text

# MP3 파일을 분할하는 함수
def split_audio(mp3_path, chunk_duration=3600):
    print(f"[🔄] {mp3_path} 파일 분할 시작...")
    try:
        # output_mp3 폴더가 없으면 생성
        os.makedirs('output_mp3', exist_ok=True)
        
        # mp3 파일을 1시간씩 나누는 예시 (1시간 = 3600초)
        command = ['ffmpeg', '-i', mp3_path, '-f', 'segment', '-segment_time', str(chunk_duration), '-c', 'copy', 'output_mp3/output%03d.mp3']
        subprocess.run(command, check=True)
        print("[✔] 파일 분할 완료.")
    except subprocess.CalledProcessError as e:
        print(f"[❌] 오류 발생: {e}")

# 텍스트 파일 저장 함수
def save_text(text, text_filename):
    print(f"[📝] 텍스트 저장 시작: {text_filename}")
    os.makedirs(os.path.dirname(text_filename), exist_ok=True)
    with open(text_filename, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"[✔] 텍스트 저장 완료: {text_filename}")

# 모든 작업을 병렬로 처리하는 함수
def process_audio(mp3_path, chunk_duration=3600, sample_rate=16000):
    print(f"[🔄] {mp3_path} 처리 시작...")
    # MP3 파일 분할
    split_audio(mp3_path, chunk_duration)

    # 분할된 MP3 파일들에 대해 WAV로 변환 및 텍스트 추출
    mp3_files = [f"output_mp3/output{str(i).zfill(3)}.mp3" for i in range(len(os.listdir('output_mp3')))]  # 분할된 MP3 파일들
    
    # output_wav, output_text 폴더가 없으면 생성
    os.makedirs('output_wav', exist_ok=True)
    os.makedirs('output_text', exist_ok=True)

    with ThreadPoolExecutor() as executor:
        # 각 MP3 파일을 WAV로 변환하는 작업 병렬 처리
        futures = []
        for mp3_file in mp3_files:
            wav_file = mp3_file.replace('output_mp3', 'output_wav').replace('.mp3', '.wav')
            futures.append(executor.submit(mp3_to_wav, mp3_file, wav_file, sample_rate))

        # WAV로 변환 완료된 파일들에 대해 텍스트 추출
        for future in futures:
            future.result()  # WAV 변환 완료 후

        # 텍스트 추출 및 저장
        text_futures = []
        for wav_file in mp3_files:
            wav_file = wav_file.replace('output_mp3', 'output_wav').replace('.mp3', '.wav')
            text_filename = wav_file.replace('output_wav', 'output_text').replace('.wav', '.txt')
            text_futures.append(executor.submit(extract_text_from_wav, wav_file))

        # 텍스트 저장
        for idx, future in enumerate(text_futures):
            text = future.result()
            text_filename = mp3_files[idx].replace('output_mp3', 'output_text').replace('.mp3', '.txt')
            save_text(text, text_filename)

if __name__ == "__main__":
    mp3_path = 'input_mp3/youtube_output.mp3'  # 예시 파일 경로
    process_audio(mp3_path, chunk_duration=3600, sample_rate=16000)
