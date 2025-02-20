import speech_recognition as sr
import pyttsx3
import threading
import sys
from PyQt6.QtWidgets import QApplication
from core.openai_api import get_ai_response

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speech speed

# Set Male English (US) Voice - Microsoft David
selected_voice = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0"
engine.setProperty('voice', selected_voice)
print(f"✅ Using voice: Microsoft David (US Male)")

# Global flag for exiting
exit_flag = False

def speak(text: str):
    """
    Convert text to speech and play it.
    """
    global exit_flag

    if text:
        def run():
            engine.say(text)
            engine.runAndWait()

        speech_thread = threading.Thread(target=run)
        speech_thread.start()
        speech_thread.join()  # Ensure speech finishes before next action

def listen() -> str:
    """
    Capture audio from the user and convert it to text.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Faster noise calibration
        recognizer.energy_threshold = 300  # Reduce background noise detection
        recognizer.dynamic_energy_threshold = True  # Auto-adjust sensitivity
        print("🎤 Listening...")

        try:
            audio = recognizer.listen(source, timeout=3)  # Short timeout for quick detection
            user_input = recognizer.recognize_google(audio).lower()
            print(f"🔍 Heard: {user_input}")

            return user_input

        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return "Error: Could not reach speech recognition service."
        except sr.WaitTimeoutError:
            return ""

def main():
    """
    AI assistant listens for 'Frosty' and stays in conversation mode.
    """
    global exit_flag

    print("❄️ Frosty is always ready. Say 'Frosty' to wake me.")
    speak("Hello! Say 'Frosty' to activate me.")

    while not exit_flag:
        user_input = listen()  # Always listen
        if "frosty" in user_input:
            speak("How can I assist you?")
            handle_commands()  # Enter conversation mode

def handle_commands():
    """Listens for multiple AI commands after wake word is detected."""
    global exit_flag

    while not exit_flag:
        command = listen()
        if command in ["exit", "quit", "stop"]:
            speak("Goodbye! Have a great day!")
            exit_flag = True
            QApplication.quit()  # Properly exit the application
            return

        if command:  # Ensure command is not empty
            response = get_ai_response(command)
            print(f"🤖 Frosty: {response}")
            speak(response)  # AI keeps listening after response
