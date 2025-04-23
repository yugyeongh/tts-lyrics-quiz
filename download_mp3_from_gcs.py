from google.cloud import storage

# 서비스 계정 키 파일로 클라이언트 생성
client = storage.Client.from_service_account_json("key.json")

# 버킷 이름과 파일 이름 지정
bucket_name = "bucket-tts-quiz"
source_blob_name = "youtube_output.mp3"
destination_file_name = "youtube_output.mp3"  # RunPod에 저장할 이름

# 버킷 접근 후 파일 다운로드
bucket = client.get_bucket(bucket_name)
blob = bucket.blob(source_blob_name)
blob.download_to_filename(destination_file_name)

print(f"Downloaded '{source_blob_name}' to '{destination_file_name}'.")
