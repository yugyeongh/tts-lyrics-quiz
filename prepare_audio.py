import os
from dotenv import load_dotenv
import yt_dlp

def load_environment_variable():
    load_dotenv()
    URL = os.getenv("YOUTUBE_URL")
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'input_mp3')
    OUTPUT_FILENAME = os.getenv('OUTPUT_FILENAME', 'youtube_output.mp3')

    return URL, OUTPUT_DIR, OUTPUT_FILENAME

def ensure_output_directory_exists(output_dir):
    os.makedirs(output_dir, exist_ok=True)

def get_output_file_path(output_dir, output_filename):
    return os.path.join(output_dir, output_filename)

def get_ydl_opts(output_file_path):
    return {
        'format': 'bestaudio/best',
        'outtmpl': output_file_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

def download_mp3(url, output_dir, output_filename):
    ensure_output_directory_exists(output_dir)
    output_file_path = get_output_file_path(output_dir, output_filename)

    ydl_opts = get_ydl_opts(output_file_path)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"{output_file_path} 다운로드 완료")
    except Exception as e:
        print(f"다운로드 중 오류 발생: {e}")
        raise

    return output_file_path

if __name__ == '__main__':
    URL, OUTPUT_DIR, OUTPUT_FILENAME = load_environment_variable()

    try:
        output_file = download_mp3(URL, OUTPUT_DIR, OUTPUT_FILENAME)
        print(f'{output_file} 끝')
    except Exception as e:
        print(f"프로세스 중 오류가 발생했습니다: {e}")
