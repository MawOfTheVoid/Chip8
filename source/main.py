from PySide2.QtWidgets import QApplication
from chip8_launcher import Launcher
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher_window = Launcher()
    sys.exit(app.exec_())