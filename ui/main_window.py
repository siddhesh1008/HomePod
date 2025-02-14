import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt6.QtGui import QPixmap, QRegion
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

        # Set fixed size for Windows testing
        self.setGeometry(100, 100, 1080, 1080)
        self.setWindowTitle("AI Assistant")

        # Make the window fullscreen automatically
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.showMaximized()  # Maximized for testing

        # Apply Circular Mask (DISABLED for Windows testing)
        # Uncomment before deploying to Raspberry Pi
        # self.setMask(QRegion(0, 0, 1080, 1080, QRegion.RegionType.Ellipse))

        # Set Background Image
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap("assets/background.jpg"))
        self.bg_label.setGeometry(0, 0, 1080, 1080)

        # Live Clock Widget
        self.clock_label = QLabel("00:00:00", self)
        self.clock_label.setStyleSheet("color: white; font-size: 40px;")
        self.clock_label.setGeometry(450, 50, 200, 50)

        # Timer for Updating Clock
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        # AI Chat Output
        self.chat_output = QTextEdit(self)
        self.chat_output.setGeometry(150, 200, 780, 150)
        self.chat_output.setStyleSheet("background: black; color: white; border: none; font-size: 16px;")
        self.chat_output.setReadOnly(True)

        # **🎤 Voice Command Display Box**
        self.voice_display = QTextEdit(self)
        self.voice_display.setGeometry(150, 370, 780, 100)
        self.voice_display.setStyleSheet("background: #333; color: cyan; font-size: 18px; border-radius: 10px; padding: 5px;")
        self.voice_display.setReadOnly(True)
        self.voice_display.setPlainText("🎤 Speak to start...")
        self.voice_display.show()
        self.voice_display.raise_()

        # AI Chat Input
        self.chat_input = QLineEdit(self)
        self.chat_input.setGeometry(200, 500, 600, 50)
        self.chat_input.setStyleSheet("background: black; color: white; border: 2px solid white; font-size: 16px;")

        # Submit Button
        self.submit_btn = QPushButton("Ask", self)
        self.submit_btn.setGeometry(820, 500, 100, 50)
        self.submit_btn.setStyleSheet("background: gray; color: white; font-size: 18px;")
        self.submit_btn.clicked.connect(self.send_message)

        # **Voice Command Button**
        self.voice_btn = QPushButton("🎤 Voice Command", self)
        self.voice_btn.setGeometry(440, 600, 200, 60)
        self.voice_btn.setStyleSheet("background: green; color: white; font-size: 18px; border-radius: 10px;")
        self.voice_btn.clicked.connect(self.start_voice_assistant)
        self.voice_btn.show()

        # Initialize voice recognition thread
        self.voice_thread = VoiceRecognitionThread()
        self.voice_thread.recognized_text.connect(self.process_voice_command)

    def update_time(self):
        """Updates the clock display in real-time."""
        current_time = QTime.currentTime().toString("hh:mm:ss")
        self.clock_label.setText(current_time)

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
        self.voice_display.show()
        self.voice_display.raise_()
        self.voice_thread.start()

    def process_voice_command(self, user_input):
        """Processes voice command and gets AI response."""
        self.voice_display.setPlainText(f"🗣️ You: {user_input}")
        response = get_ai_response(user_input)
        self.chat_output.setPlainText(response)
        self.voice_display.append(f"🤖 AI: {response}")
        self.voice_btn.setText("🎤 Voice Command")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CircularUI()
    window.show()
    sys.exit(app.exec())
