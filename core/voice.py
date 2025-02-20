import speech_recognition as sr
import pyttsx3
import threading
import sys
from PyQt6.QtWidgets import QApplication
from core.openai_api import get_ai_response
from core.weather_api import get_weather  # Import the weather function

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speech speed

# Set Male English (US) Voice - Microsoft David
selected_voice = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0"
engine.setProperty('voice', selected_voice)
print(f"✅ Using voice: Microsoft David (US Male)")

# Global flag to exit assistant
exit_flag = False  

def speak(text: str):
    """
    Convert text to speech and play it.
    """
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
    Detects weather queries and calls the weather function directly.
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

            # **Directly Handle Weather Queries Here**
            if "weather" in user_input:
                process_weather_query(user_input)  # Call weather function immediately
                return ""  # Stop further processing

            return user_input

        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return "Error: Could not reach speech recognition service."
        except sr.WaitTimeoutError:
            return ""

def process_weather_query(command: str):
    """
    Extracts city from command, cleans unnecessary words, and fetches weather.
    """
    print("🛠 DEBUG: Processing weather query!")  # Debug message
    city = ""

    # Extract city name (everything after "in")
    words = command.split()
    if "in" in words:
        city_index = words.index("in") + 1
        if city_index < len(words):  # Ensure city exists after "in"
            city = " ".join(words[city_index:])

    # **Clean city name (remove words like "today", "tomorrow")**
    words_to_remove = ["today", "tomorrow", "right now", "currently", "now"]
    city = " ".join([word for word in city.split() if word not in words_to_remove])

    # If no city was detected, ask the user for a city name
    if not city or len(city) < 2:  # Prevents invalid city names
        speak("Which city would you like the weather for?")
        city = listen().strip()  # Listen again for a city name
        print(f"🛠 DEBUG: User provided city -> {city}")

    # If still no city is detected, return an error
    if not city or len(city) < 2:
        speak("I still didn't get a city name. Please try again.")
        return  # **Stops further AI processing after weather response**

    print(f"🌍 DEBUG: Fetching weather for -> {city}")  # Debug message
    weather_response = get_weather(city)  # Fetch real-time weather data
    print(f"🤖 DEBUG: Weather API Response -> {weather_response}")  # Debug message
    speak(weather_response)  # Speak the actual weather report

    return  # **Ensures AI does NOT process any further after weather query**

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

        # **Process OpenAI commands ONLY if it's NOT a weather query**
        if "weather" not in command:  # Ensures OpenAI API is NEVER called after weather
            print("🛠 DEBUG: Sending command to OpenAI")  # Debug message
            response = get_ai_response(command)
            speak(response)  # AI keeps listening after response
