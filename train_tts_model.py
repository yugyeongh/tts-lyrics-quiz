import os
import sys
sys.path.append('./hifi-gan')
import torch
import torchaudio
import numpy as np
from torch.utils.data import Dataset
import torch.nn as nn
import torch.optim as optim
from torchaudio.transforms import MelSpectrogram
from hifi_gan import HiFiGAN  # HiFi-GAN 모델을 임포트 (실제 구현을 가정)

# 텍스트를 인덱스 시퀀스로 변환하는 함수
def text_to_sequence(text, vocab):
    return [vocab.get(char, vocab['<unk>']) for char in text]

# Dataset 클래스 정의
class TTSDataset(Dataset):
    def __init__(self, wav_dir, text_dir, vocab):
        self.wav_dir = wav_dir
        self.text_dir = text_dir
        self.vocab = vocab
        self.wav_files = [f for f in os.listdir(wav_dir) if f.endswith('.wav')]
        self.text_files = [f.replace('.wav', '.txt') for f in self.wav_files]

    def __len__(self):
        return len(self.wav_files)

    def __getitem__(self, idx):
        wav_file = self.wav_files[idx]
        text_file = self.text_files[idx]
        
        # WAV 파일 로드
        wav_path = os.path.join(self.wav_dir, wav_file)
        waveform, sample_rate = torchaudio.load(wav_path)
        
        # 텍스트 파일 로드
        text_path = os.path.join(self.text_dir, text_file)
        with open(text_path, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        
        # 텍스트를 인덱스로 변환
        text_seq = text_to_sequence(text, self.vocab)

        return waveform, torch.tensor(text_seq)

# WAV 파일을 멜-스펙트로그램으로 변환하는 함수
def wav_to_mel_spectrogram(waveform, sample_rate, n_mels=80):
    mel_transform = MelSpectrogram(sample_rate=sample_rate, n_mels=n_mels)
    mel_spec = mel_transform(waveform)
    return mel_spec

# Tacotron2 모델 정의
class Tacotron2(nn.Module):
    def __init__(self, vocab_size, hidden_dim=256):
        super(Tacotron2, self).__init__()
        self.embedding = nn.Embedding(vocab_size, hidden_dim)
        self.rnn = nn.LSTM(hidden_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, 80)  # 멜-스펙트로그램 크기 (80)

    def forward(self, x):
        x = self.embedding(x)
        x, _ = self.rnn(x)
        mel_spec = self.fc(x)
        return mel_spec

# HiFi-GAN Vocoder 정의 (실제 모델 로드 및 사용)
class HiFiGANVocoder(nn.Module):
    def __init__(self, model_path):
        super(HiFiGANVocoder, self).__init__()
        self.model = HiFiGAN.load(model_path)  # HiFi-GAN 모델을 로드

    def forward(self, mel_spec):
        audio = self.model.generate_audio(mel_spec)  # 멜-스펙트로그램을 파형으로 변환
        return audio

# 학습 루프 정의
def train_tts_model():
    # 데이터셋 준비 (간단한 문자 -> 인덱스 맵 예시)
    vocab = {'<unk>': 0, '안': 1, '녕': 2, '하': 3, '세': 4, '요': 5}
    dataset = TTSDataset('output_wav', 'output_text', vocab)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=16, shuffle=True)  # 배치 크기 16으로 조정

    # 모델 및 Vocoder 초기화
    tacotron_model = Tacotron2(vocab_size=len(vocab))  # Tacotron2 모델
    vocoder = HiFiGANVocoder(model_path='hifi_gan_model.pth')  # HiFi-GAN 모델 불러오기

    # 옵티마이저와 손실 함수 정의
    optimizer = torch.optim.Adam(tacotron_model.parameters(), lr=1e-4)

    # 혼합 정밀도 학습을 위한 설정
    scaler = torch.cuda.amp.GradScaler()

    # 학습 루프
    for epoch in range(10):  # 10 epochs 동안 학습
        print(f"Epoch [{epoch+1}/10] 시작")
        for waveform, text_seq in dataloader:
            print("배치 처리 시작")
            optimizer.zero_grad()

            # 혼합 정밀도 학습 적용
            with torch.cuda.amp.autocast():
                # 텍스트 -> 멜-스펙트로그램 예측
                predicted_mel = tacotron_model(text_seq)

                # 멜-스펙트로그램 -> 음성 파형 생성
                audio = vocoder(predicted_mel)

                # 손실 계산 (MSELoss 사용)
                loss = nn.MSELoss()(audio, waveform)

            # 역전파 및 가중치 업데이트
            scaler.scale(loss).backward()  # 역전파
            scaler.step(optimizer)  # 가중치 업데이트
            scaler.update()  # GradScaler 업데이트

            print(f"배치 처리 완료, Loss: {loss.item()}")

        # 에포크 끝날 때 모델 저장
        save_model(tacotron_model, epoch)
        print(f"Epoch [{epoch+1}/10] 완료")

# 모델 저장 함수
def save_model(model, epoch, save_dir='saved_models'):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    model_path = os.path.join(save_dir, f'tts_model_epoch_{epoch+1}.pth')
    torch.save(model.state_dict(), model_path)  # 모델 가중치 저장
    print(f"Model saved to {model_path}")

# 텍스트를 음성으로 변환하여 저장하는 함수
def synthesize_and_save_audio(text, tacotron_model, vocoder, vocab, output_path='output_audio.wav'):
    tacotron_model.eval()  # 모델을 평가 모드로 전환
    print("음성 생성 시작")

    # 텍스트를 인덱스 시퀀스로 변환
    text_seq = torch.tensor(text_to_sequence(text, vocab)).unsqueeze(0)  # 배치 차원 추가

    # 멜-스펙트로그램 예측
    with torch.no_grad():
        mel_spec = tacotron_model(text_seq)

    # 멜-스펙트로그램을 음성 파형으로 변환
    audio = vocoder(mel_spec)

    # 음성을 저장
    torchaudio.save(output_path, audio.squeeze(0), 22050)  # 22050 Hz 샘플링 주파수로 저장
    print(f"Generated audio saved to {output_path}")

# 모델을 로드하여 텍스트를 음성으로 변환 후 저장하는 예시
def load_model_and_synthesize():
    vocab = {'<unk>': 0, '안': 1, '녕': 2, '하': 3, '세': 4, '요': 5}
    tacotron_model = Tacotron2(vocab_size=len(vocab))
    tacotron_model.load_state_dict(torch.load('saved_models/tts_model_epoch_10.pth'))  # 모델 로드
    vocoder = HiFiGANVocoder(model_path='hifi_gan_model.pth')  # HiFi-GAN 로드

    # 텍스트를 음성으로 변환하여 저장
    text = "안녕하세요, 반갑습니다!"
    synthesize_and_save_audio(text, tacotron_model, vocoder, vocab)

if __name__ == "__main__":
    # 학습 후 모델 저장이 끝나면 이 함수를 호출
    load_model_and_synthesize()
