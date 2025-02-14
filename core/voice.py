import speech_recognition as sr

# Set this to a specific mic index if needed (Run mic check script if unsure)
MICROPHONE_INDEX = None  # Change this if default mic is not working

def recognize_speech():
    """Captures audio and converts it to text using SpeechRecognition with noise filtering."""
    recognizer = sr.Recognizer()

    # Use a specific microphone if the default is not working
    mic_source = sr.Microphone(device_index=MICROPHONE_INDEX) if MICROPHONE_INDEX is not None else sr.Microphone()

    with mic_source as source:
        # Noise reduction setup
        recognizer.adjust_for_ambient_noise(source, duration=2.0)  # Longer calibration for better filtering
        recognizer.energy_threshold = 400  # Filters out unwanted background noise
        recognizer.dynamic_energy_threshold = True  # Auto-adjusts to real-time noise
        recognizer.pause_threshold = 0.8  # Ensures quick response time without cutting off speech

        try:
            # Listen for speech with timeout
            audio = recognizer.listen(source, timeout=6)  
            return recognizer.recognize_google(audio).lower()  # Convert speech to text
        
        except sr.WaitTimeoutError:
            return None  # No speech detected
        except sr.UnknownValueError:
            return None  # Speech not clear
        except sr.RequestError:
            return None  # API issue or no internet
