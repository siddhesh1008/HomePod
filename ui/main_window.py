import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt6.QtGui import QPixmap, QFont, QRegion, QMovie
from PyQt6.QtCore import Qt, QTimer, QTime, QThread, pyqtSignal
from core.openai_api import get_ai_response
from core.voice import recognize_speech

class VoiceRecognitionThread(QThread):
    """Handles voice recognition in a separate thread to prevent UI freezing."""
    recognized_text = pyqtSignal(str)  # Signal to update the UI

    def run(self):
        user_input = recognize_speech()  # Get spoken text
        if user_input:
            self.recognized_text.emit(user_input)  # Send text to main UI

class CircularUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load Custom QSS Styling
        with open("ui/styles.qss", "r") as f:
            self.setStyleSheet(f.read())

        # Set Circular Window (For Waveshare 5-inch round display)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(100, 100, 1080, 1080)
        self.setMask(QRegion(0, 0, 1080, 1080, QRegion.RegionType.Ellipse))
        self.showFullScreen()

        # 🎥 Set Animated GIF Background
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, 1080, 1080)

        # Load GIF as Background
        self.bg_movie = QMovie("assets/background.gif")  # Ensure this file exists!
        self.bg_movie.setScaledSize(self.bg_label.size())  # Scale properly
        self.bg_label.setMovie(self.bg_movie)
        self.bg_movie.start()  # Start animation
        self.bg_label.lower()  # Ensure it's in the background

        # Ensure Background is Visible
        self.bg_label.show()
        self.bg_label.repaint()

        # ⏰ Live Clock Widget (Balanced Position)
        self.clock_label = QLabel("00:00:00", self)
        self.clock_label.setFont(QFont("Arial", 55, QFont.Weight.Bold))  # Slightly smaller
        self.clock_label.setGeometry(340, 100, 400, 80)  # Moved lower
        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.clock_label.setStyleSheet("color: white; background: none; font-size: 55px; font-weight: bold;")
        self.clock_label.raise_()
        self.clock_label.show()
        self.clock_label.repaint()

        # Timer for Updating Clock
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        # 📌 AI Chat Output Box
        self.chat_output = QTextEdit(self)
        self.chat_output.setGeometry(150, 250, 780, 150)
        self.chat_output.setReadOnly(True)

        # 🎤 Voice Command Display Box (Fixed Text Color)
        self.voice_display = QTextEdit(self)
        self.voice_display.setGeometry(150, 430, 780, 70)
        self.voice_display.setReadOnly(True)
        self.voice_display.setPlainText("🎤 Speak to start...")
        self.voice_display.setStyleSheet("background: rgba(20, 20, 20, 120); color: white; border-radius: 15px;")
        self.voice_display.show()
        self.voice_display.raise_()
        self.voice_display.repaint()

        # 📌 AI Chat Input Box
        self.chat_input = QLineEdit(self)
        self.chat_input.setGeometry(200, 550, 600, 50)

        # 🟢 Submit Button
        self.submit_btn = QPushButton("Ask", self)
        self.submit_btn.setGeometry(820, 550, 100, 50)
        self.submit_btn.clicked.connect(self.send_message)

        # 🎤 Voice Command Button (Blends with UI Better)
        self.voice_btn = QPushButton("🎤 Voice Command", self)
        self.voice_btn.setGeometry(420, 650, 240, 70)
        self.voice_btn.setStyleSheet("background-color: rgba(0, 200, 200, 180); color: white; border-radius: 20px; font-size: 22px;")
        self.voice_btn.clicked.connect(self.start_voice_assistant)
        self.voice_btn.show()

        # Initialize voice recognition thread
        self.voice_thread = VoiceRecognitionThread()
        self.voice_thread.recognized_text.connect(self.process_voice_command)

    def update_time(self):
        """Updates the clock display in real-time."""
        current_time = QTime.currentTime().toString("hh:mm:ss")
        self.clock_label.setText(current_time)
        self.clock_label.repaint()

    def send_message(self):
        """Sends user input to OpenAI and displays the response."""
        user_input = self.chat_input.text()
        self.voice_display.setPlainText(f"🗣️ You: {user_input}")
        response = get_ai_response(user_input)
        self.chat_output.setPlainText(response)
        self.voice_display.append(f"🤖 AI: {response}")

    def start_voice_assistant(self):
        """Starts voice assistant in a separate thread to prevent UI freeze."""
        self.voice_btn.setText("Listening...")
        self.voice_display.setPlainText("🎤 Listening... Speak now!")
        self.voice_display.repaint()
        self.voice_thread.start()

    def process_voice_command(self, user_input):
        """Processes voice command and gets AI response."""
        self.voice_display.setPlainText(f"🗣️ You: {user_input}")
        response = get_ai_response(user_input)
        self.chat_output.setPlainText(response)
        self.voice_display.append(f"🤖 AI: {response}")
        self.voice_display.repaint()
        self.voice_btn.setText("🎤 Voice Command")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CircularUI()
    window.show()
    sys.exit(app.exec())
