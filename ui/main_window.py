import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QFont, QMovie, QRegion
from PyQt6.QtCore import Qt, QTimer, QTime, QThread
from core.voice import speak, listen
from core.spotify_api import play_music, pause_music, next_track, previous_track, play_specific_song  # Import Spotify controls

class HotwordDetectionThread(QThread):
    """Continuously listens for 'Frosty' in a separate thread."""

    def run(self):
        print("🎙️ Hotword Detection Thread Started...")
        speak("Hello! Say 'Frosty' to activate me.")
        while True:
            user_input = listen()
            if "frosty" in user_input:
                print("✅ Hotword Detected: 'Frosty'")
                speak("I am listening. How can I assist you?")
                self.start_voice_assistant()

    def start_voice_assistant(self):
        """Handles voice recognition and AI response through voice only."""
        while True:
            user_input = listen()
            if user_input in ["exit", "quit", "stop"]:
                speak("Goodbye! Have a great day!")
                print("❌ Exiting...")
                return

            # Spotify Commands
            if "play music" in user_input:
                response = play_music()
            elif "pause music" in user_input:
                response = pause_music()
            elif "next song" in user_input or "skip" in user_input:
                response = next_track()
            elif "previous song" in user_input:
                response = previous_track()
            elif "play" in user_input:
                song_name = user_input.replace("play", "").strip()
                response = play_specific_song(song_name)
            else:
                # Default to AI response
                from core.openai_api import get_ai_response
                response = get_ai_response(user_input)

            print(f"🤖 Frosty: {response}")
            speak(response)

class CircularUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load Custom QSS Styling
        with open("ui/styles.qss", "r") as f:
            self.setStyleSheet(f.read())

        # Set Circular Window Shape
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(100, 100, 1080, 1080)
        self.setMask(QRegion(0, 0, 1080, 1080, QRegion.RegionType.Ellipse))
        self.showFullScreen()

        # 🎥 Set Animated GIF Background
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, 1080, 1080)
        self.bg_movie = QMovie("assets/background.gif")
        self.bg_movie.setScaledSize(self.bg_label.size())
        self.bg_label.setMovie(self.bg_movie)
        self.bg_movie.start()
        self.bg_label.lower()
        self.bg_label.show()
        self.bg_label.repaint()

        # ⏰ Live Clock Widget
        self.clock_label = QLabel("00:00:00", self)
        self.clock_label.setFont(QFont("Arial", 60, QFont.Weight.Bold))
        self.clock_label.setGeometry(340, 50, 400, 80)
        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.clock_label.setStyleSheet("color: white; background: none; font-size: 60px; font-weight: bold;")
        self.clock_label.show()

        # Timer for Updating Clock
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        # Start AI assistant in a separate thread
        self.hotword_thread = HotwordDetectionThread()
        self.hotword_thread.start()

    def update_time(self):
        """Updates the clock display in real-time."""
        current_time = QTime.currentTime().toString("hh:mm:ss")
        self.clock_label.setText(current_time)
        self.clock_label.repaint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CircularUI()
    window.show()
    sys.exit(app.exec())
