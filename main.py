import cv2
import torch
import numpy as np
import sounddevice as sd
from datetime import datetime
from serial import Serial
import speech_recognition as sr
import requests
import random
import time
import platform

# Setup Arduino
try:
    arduino = Serial('/dev/ttyUSB3', 9600)
    time.sleep(2)
except Exception as e:
    print(f"Error connecting to Arduino: {e}")
    arduino = None

# Speech Recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5)
            return recognizer.recognize_google(audio).lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        return ""
    except sr.WaitTimeoutError:
        print("Listening timed out while waiting for speech.")
        return ""

# NLP Functions
def greet():
    greetings = [
        "Hello there!",
        "Hi there!",
        "How are you doing?",
        "What's up?",
        "How's it going?",
        "What's new?",
        "How can I assist you?"
    ]
    return random.choice(greetings)

def get_time():
    return datetime.now().strftime("%H:%M:%S")

def get_date():
    return datetime.now().strftime("%Y-%m-%d")

def get_day():
    return datetime.now().strftime("%A")

def get_weather():
    api_key = "ec0770004c8f43478fa160700242711"
    city = "Bangalore"
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
    try:
        response = requests.get(url).json()
        if "current" in response:
            temp = response["current"]["temp_c"]
            condition = response["current"]["condition"]["text"]
            return f"{temp}°C, {condition}"
        return "Weather data unavailable."
    except Exception as e:
        return f"Error fetching weather: {e}"

def get_news():
    api_key = "01dff69893a84b309176964d2176e509"
    url = f"https://newsapi.org/v2/top-headlines?apiKey={api_key}"
    try:
        response = requests.get(url).json()
        articles = response.get("articles", [])
        if articles:
            news = [article["title"] for article in articles[:3]]
            return " | ".join(news)
        return "No news available."
    except Exception as e:
        return f"Error fetching news: {e}"

def get_quote():
    url = "https://zenquotes.io/api/quotes"
    try:
        response = requests.get(url).json()
        return response[0]["q"]
    except Exception as e:
        return f"Error fetching quote: {e}"

def display_on_mirror(output):
    if arduino:
        print(f"Sending to Arduino: {output}")
        arduino.write(f"{output}\n".encode())

# Initialize Camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Camera not detected!")
    exit()

print("Smart Mirror is running...")

try:
    while True:
        transcription = recognize_speech()
        print(f"Speech recognized: {transcription}")

        if "time" in transcription:
            response = get_time()
        elif "date" in transcription:
            response = get_date()
        elif "day" in transcription:
            response = get_day()
        elif "weather" in transcription:
            response = get_weather()
        elif "news" in transcription:
            response = get_news()
        elif "motivat" in transcription or "quote" in transcription:
            response = get_quote()
        elif "hi" in transcription or "hello" in transcription or "hey" in transcription:
            response = greet()
        else:
            response = ""

        print(f"Response: {response}")

        display_on_mirror(response)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    cap.release()
    cv2.destroyAllWindows()
    if arduino:
        arduino.close()
