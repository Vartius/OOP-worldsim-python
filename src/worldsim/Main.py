import os
import sys
from PyQt6.QtWidgets import QApplication
from worldsim.world.World import World
from windowManager.Winman import WindowManager

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    app = QApplication(sys.argv)
    w = World()
    ex = WindowManager(w)
    w.setWindowManager(ex)
    app.setStyleSheet(
        """
        QWidget {
            background-color: #2b2b2b;
            color: #b1b1b1;
        }
        QPushButton {
            background-color: #333333;
            border: 1px solid #4A4949;
            border-radius: 2px;awd
            color: #b1b1b1;
        }
        QPushButton:hover {
            background-color: #4A4949;
        }
        QPushButton:pressed {
            background-color: #5A5A5A;
        }
        QLineEdit {
            background-color: #333333;
            color: #b1b1b1;
            border: 1px solid #4A4949;
            border-radius: 2px;
        }
    """
    )
    sys.exit(app.exec())
