from PyQt6.QtWidgets import QApplication
import sys
from ui.main_window import CircularUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CircularUI()
    window.show()
    sys.exit(app.exec())
