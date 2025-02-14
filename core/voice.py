import speech_recognition as sr
import pyttsx3
from core.openai_api import get_ai_response

# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 160)  # Adjust speaking speed
tts_engine.setProperty("volume", 1.0)  # Set volume level

def speak(text):
    """Converts text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()

def recognize_speech():
    """Captures audio and converts it to text using SpeechRecognition."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Reduce noise
        try:
            audio = recognizer.listen(source, timeout=5)  # Listen for 5 seconds
            command = recognizer.recognize_google(audio)  # Convert to text
            print(f"🗣️ Recognized: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            print("⏳ No speech detected...")
            return None
        except sr.UnknownValueError:
            print("🤷 Could not understand the audio...")
            return None
        except sr.RequestError:
            print("⚠️ API unavailable. Check your internet connection.")
            return None

def voice_assistant():
    """Main loop for listening to commands and responding."""
    while True:
        command = recognize_speech()
        if command:
            if "exit" in command or "stop" in command:
                speak("Goodbye!")
                break
            response = get_ai_response(command)  # Send text to AI assistant
            print(f"🤖 AI Response: {response}")
            speak(response)  # Speak the response
