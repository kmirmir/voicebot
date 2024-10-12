import os
from dotenv import load_dotenv
import streamlit as st
import speech_recognition as sr
import pyttsx3
import openai
import threading

# .env 파일 로드
load_dotenv()

# OpenAI API 설정
# openai.api_key = os.getenv("OPENAI_API_KEY")

# 음성 인식을 위한 설정
recognizer = sr.Recognizer()

# Streamlit 앱 UI 구성
st.title("ChatGPT 음성 기반 AI 챗봇")
st.write("마이크 버튼을 눌러 음성 입력을 시작하세요.")

# 마이크로 음성 입력 받기
def recognize_speech():
    with sr.Microphone() as source:
        st.write("듣고 있습니다...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            st.write("음성 인식 중...")
            text = recognizer.recognize_google(audio, language="ko-KR")
            st.write(f"입력된 텍스트: {text}")
            return text
        except sr.UnknownValueError:
            st.write("음성을 인식할 수 없습니다.")
        except sr.RequestError:
            st.write("음성 인식 서비스에 연결할 수 없습니다.")
        return ""

# GPT-4 API로 응답 생성 (Chat API 엔드포인트 사용)
def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # GPT-4 모델 사용
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    return response['choices'][0]['message']['content'].strip()

# 음성 출력 (쓰레드를 사용하여 실행)
def speak_text(text):
    def run_speech():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    # 새로운 쓰레드에서 음성 출력 실행
    speech_thread = threading.Thread(target=run_speech)
    speech_thread.start()

# 버튼을 누르면 음성 인식을 시작
if st.button("음성 입력 시작 버튼"):
    user_input = recognize_speech()
    if user_input:
        # ChatGPT로부터 응답 생성
        response = generate_response(user_input)
        st.write(f"ChatGPT의 응답: {response}")
        
        # 응답을 음성으로 출력
        speak_text(response)

# Streamlit 앱 실행
st.write("음성 입력을 기다리고 있습니다...")

