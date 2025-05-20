import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QTextEdit, QStackedWidget
from PyQt6.QtGui import QFont, QMovie, QRegion, QPixmap, QTransform, QPainter, QIcon
from PyQt6.QtCore import Qt, QTimer, QTime

from core.weather_api import get_weather
from core.spotify_api import play_music, play_specific_song, pause_music, next_track, previous_track, get_spotify_client

# ------------------ Home Screen ------------------
class HomeScreen(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Background GIF
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, 1080, 1080)
        self.bg_movie = QMovie("assets/background.gif")
        self.bg_movie.setScaledSize(self.bg_label.size())
        self.bg_label.setMovie(self.bg_movie)
        self.bg_movie.start()
        self.bg_label.lower()

        # Clock
        self.clock_label = QLabel("00:00:00", self)
        self.clock_label.setFont(QFont("Arial", 60, QFont.Weight.Bold))
        self.clock_label.setGeometry(340, 50, 400, 80)
        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.clock_label.setStyleSheet("color: white; background: none; font-weight: bold;")

        # Timer for clock
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        # Weather Display
        self.weather_display = QTextEdit(self)
        self.weather_display.setGeometry(250, 500, 580, 200)
        self.weather_display.setFont(QFont("Arial", 20))
        self.weather_display.setStyleSheet("background: rgba(0,0,0,150); color: white; border-radius: 20px;")
        self.weather_display.setReadOnly(True)
        self.weather_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weather_display.setText("Tap an icon to get started!")

        # Weather Button
        self.weather_btn = QPushButton(self)
        self.weather_btn.setGeometry(270, 300, 150, 150)
        if os.path.exists("assets/weather_icon.png"):
            self.weather_btn.setIcon(QIcon("assets/weather_icon.png"))
            self.weather_btn.setIconSize(self.weather_btn.size())
        self.weather_btn.setStyleSheet("border: none; background: transparent;")
        self.weather_btn.clicked.connect(parent.show_weather)

        # Spotify Button
        self.spotify_btn = QPushButton(self)
        self.spotify_btn.setGeometry(670, 300, 150, 150)
        if os.path.exists("assets/spotify_icon.png"):
            self.spotify_btn.setIcon(QIcon("assets/spotify_icon.png"))
            self.spotify_btn.setIconSize(self.spotify_btn.size())
        self.spotify_btn.setStyleSheet("border: none; background: transparent;")
        self.spotify_btn.clicked.connect(parent.show_vinyl)

    def update_time(self):
        current_time = QTime.currentTime().toString("hh:mm:ss")
        self.clock_label.setText(current_time)
        self.clock_label.repaint()

# ------------------ Vinyl Screen ------------------
class VinylScreen(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Solid Black Background
        self.setStyleSheet("background-color: black;")

        # Vinyl Image as Background (cover full screen)
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, 1080, 1080)
        self.bg_movie = QMovie("assets/background.gif")
        self.bg_movie.setScaledSize(self.bg_label.size())
        self.bg_label.setMovie(self.bg_movie)
        self.bg_movie.start()
        self.bg_label.lower()

        # Vinyl Image (Scale to fit the screen size)
        self.original_vinyl = QPixmap("assets/vinyl.png").scaled(1080, 1080, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.vinyl_size = 1080  # Fit vinyl to screen
        self.angle = 0

        # Vinyl Display (center the vinyl)
        self.vinyl_label = QLabel(self)
        self.vinyl_label.setGeometry(0, 0, 1080, 1080)
        self.vinyl_label.setStyleSheet("background: transparent;")

        # Song Info (below vinyl animation)
        self.track_label = QLabel("Loading...", self)
        self.track_label.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        self.track_label.setGeometry(100, 950, 880, 60)
        self.track_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.track_label.setStyleSheet("color: white; background: none;")

        # Home Button (centered at top of the screen)
        self.home_btn = QPushButton(self)
        button_size = 70
        center_x = (1080 - button_size) // 2
        self.home_btn.setGeometry(center_x, 50, button_size, button_size)
        if os.path.exists("assets/home_icon.png"):
            self.home_btn.setIcon(QIcon("assets/home_icon.png"))
            self.home_btn.setIconSize(self.home_btn.size())
        self.home_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 35px;
                border: none;
            }
        """)
        self.home_btn.clicked.connect(parent.show_home)

        # --- Control Buttons Below Vinyl ---
        # Previous Button
        self.prev_btn = QPushButton(self)
        self.prev_btn.setGeometry(100, 1050, 80, 80)
        if os.path.exists("assets/previous_icon.png"):
            self.prev_btn.setIcon(QIcon("assets/previous_icon.png"))
            self.prev_btn.setIconSize(self.prev_btn.size())
        self.prev_btn.setStyleSheet("border: none; background: transparent;")
        self.prev_btn.clicked.connect(self.previous_track)

        # Play Button
        self.play_btn = QPushButton(self)
        self.play_btn.setGeometry(400, 1050, 80, 80)
        if os.path.exists("assets/play_icon.png"):
            self.play_btn.setIcon(QIcon("assets/play_icon.png"))
            self.play_btn.setIconSize(self.play_btn.size())
        self.play_btn.setStyleSheet("border: none; background: transparent;")
        self.play_btn.clicked.connect(self.play_music)

        # Pause Button
        self.pause_btn = QPushButton(self)
        self.pause_btn.setGeometry(400, 1050, 80, 80)
        if os.path.exists("assets/pause_icon.png"):
            self.pause_btn.setIcon(QIcon("assets/pause_icon.png"))
            self.pause_btn.setIconSize(self.pause_btn.size())
        self.pause_btn.setStyleSheet("border: none; background: transparent;")
        self.pause_btn.clicked.connect(self.pause_music)
        self.pause_btn.hide()  # Start hidden

        # Next Button
        self.next_btn = QPushButton(self)
        self.next_btn.setGeometry(700, 1050, 80, 80)
        if os.path.exists("assets/next_icon.png"):
            self.next_btn.setIcon(QIcon("assets/next_icon.png"))
            self.next_btn.setIconSize(self.next_btn.size())
        self.next_btn.setStyleSheet("border: none; background: transparent;")
        self.next_btn.clicked.connect(self.next_track)

        # Timers
        self.rotate_timer = QTimer(self)
        self.rotate_timer.timeout.connect(self.update_rotation)
        self.rotate_timer.start(30)

        self.track_timer = QTimer(self)
        self.track_timer.timeout.connect(self.update_track_info)
        self.track_timer.start(5000)

        play_music()

    def update_rotation(self):
        transform = QTransform()
        transform.translate(self.original_vinyl.width() / 2, self.original_vinyl.height() / 2)
        transform.rotate(self.angle)
        transform.translate(-self.original_vinyl.width() / 2, -self.original_vinyl.height() / 2)

        rotated_pixmap = self.original_vinyl.transformed(transform, Qt.TransformationMode.SmoothTransformation)

        final_pixmap = QPixmap(self.vinyl_size, self.vinyl_size)
        final_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(final_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        x_offset = (self.vinyl_size - rotated_pixmap.width()) // 2
        y_offset = (self.vinyl_size - rotated_pixmap.height()) // 2
        painter.drawPixmap(x_offset, y_offset, rotated_pixmap)
        painter.end()

        self.vinyl_label.setPixmap(final_pixmap)
        self.angle = (self.angle + 1) % 360

    def update_track_info(self):
        try:
            sp = get_spotify_client()
            playback = sp.current_playback()
            if playback and playback.get('is_playing'):
                track = playback['item']
                name = track['name']
                artist = track['artists'][0]['name']
                self.track_label.setText(f"{name} - {artist}")
        except:
            self.track_label.setText("No Track Info")

    def play_music(self):
        from core.spotify_api import play_music
        play_music()
        self.play_btn.hide()
        self.pause_btn.show()

    def pause_music(self):
        from core.spotify_api import pause_music
        pause_music()
        self.pause_btn.hide()
        self.play_btn.show()

    def next_track(self):
        from core.spotify_api import next_track
        next_track()

    def previous_track(self):
        from core.spotify_api import previous_track
        previous_track()

# ------------------ Main Controller ------------------
class CircularUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(100, 100, 1080, 1080)
        self.setMask(QRegion(0, 0, 1080, 1080, QRegion.RegionType.Ellipse))
        self.showFullScreen()

        self.stacked_widget = QStackedWidget(self)

        self.home_screen = HomeScreen(self)
        self.vinyl_screen = VinylScreen(self)

        self.stacked_widget.addWidget(self.home_screen)
        self.stacked_widget.addWidget(self.vinyl_screen)

        self.setCentralWidget(self.stacked_widget)

        self.show_home()

    def show_weather(self):
        weather_info = get_weather(os.getenv("CITY", "Berlin"))
        self.home_screen.weather_display.setText(weather_info)
        self.home_screen.weather_display.repaint()

    def show_home(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_vinyl(self):
        self.stacked_widget.setCurrentIndex(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CircularUI()
    window.show()
    sys.exit(app.exec())
