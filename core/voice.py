import speech_recognition as sr
import pyttsx3
import threading
from core.openai_api import get_ai_response

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speech speed

# Set Male English (US) Voice - Microsoft David
selected_voice = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0"
engine.setProperty('voice', selected_voice)
print(f"✅ Using voice: Microsoft David (US Male)")

# Global flag to stop speaking
stop_speaking = False

def speak(text: str):
    """
    Convert text to speech and play it. Stops if interrupted.
    """
    global stop_speaking

    if text:
        stop_speaking = False  # Reset stop flag
        def run():
            engine.say(text)
            engine.runAndWait()
        
        speech_thread = threading.Thread(target=run)
        speech_thread.start()

        # Listen while speaking to detect "Frosty" or "Exit"
        while speech_thread.is_alive():
            user_input = listen(interrupt_mode=True)
            if user_input in ["frosty", "exit", "stop"]:
                print("❌ Speech interrupted!")
                stop_speaking = True
                engine.stop()
                return  # Stop speaking and return to listening

def listen(interrupt_mode=False) -> str:
    """
    Capture audio from the user and convert it to text.
    If in interrupt mode, return immediately upon detection.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Noise calibration
        print("🎤 Listening...")

        try:
            audio = recognizer.listen(source, timeout=5)
            user_input = recognizer.recognize_google(audio).lower()
            print(f"🔍 Heard: {user_input}")

            if interrupt_mode and user_input in ["frosty", "exit", "stop"]:
                return user_input  # Stop immediately
            return user_input

        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return "Error: Could not reach speech recognition service."
        except sr.WaitTimeoutError:
            return ""

def main():
    """
    Main loop for the AI assistant using 'Frosty' as hotword.
    """
    print("❄️ Frosty is ready. Say 'Frosty' to activate.")
    speak("Hello! Say 'Frosty' to activate me.")

    while True:
        user_input = listen()
        print(f"🔍 Heard: {user_input}")

        if "frosty" in user_input:
            speak("How can I assist you?")

            while True:
                command = listen()
                print(f"🎤 You said: {command}")

                if command in ["exit", "quit", "stop"]:
                    speak("Goodbye! Have a great day!")
                    print("❌ Exiting...")
                    return

                response = get_ai_response(command)
                print(f"🤖 AI Response: {response}")
                speak(response)  # Now interruptible!

if __name__ == "__main__":
    main()
