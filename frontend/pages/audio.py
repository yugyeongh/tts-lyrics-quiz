import speech_recognition as sr

recognizer = sr.Recognizer()
target_answer = "아이유"  # 예시 정답
in_answer_mode = False  # 정답 입력 대기 상태

print("🎤 음성 인식 시작 (종료하려면 Ctrl+C)")

while True:
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("🟢 말해주세요...")
            audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio, language='ko-KR').lower()
                print("🎧 인식 결과:", text)

                if "정답" in text:
                    print("💡 정답 모드가 활성화되었습니다! 정답을 말해주세요.")
                    in_answer_mode = True
                elif in_answer_mode:
                    if target_answer.lower() in text:
                        print("✅ 정답입니다!")
                    else:
                        print("❌ 오답입니다.")
                    in_answer_mode = False  # 모드 초기화
            except sr.UnknownValueError:
                print("😅 음성을 이해하지 못했어요.")
            except sr.RequestError as e:
                print(f"🔌 요청 실패: {e}")

    except KeyboardInterrupt:
        print("\n🛑 음성 인식을 종료합니다.")
        break
