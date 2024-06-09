# file: simple_pyqt_app.py
import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout
from PyQt6.QtCore import Qt

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set default values
        self.default_world_size_x = 20
        self.default_world_size_y = 20
        self.default_organisms_count = 20

        self.initUI()

    def initUI(self):
        # Create the central widget and set it as the central widget of the QMainWindow
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Set the layout
        layout = QGridLayout()
        self.central_widget.setLayout(layout)

        # World Size X input
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(10, 10, 10, 10)
        self.world_size_x_label = QLabel('World Size X:')
        self.world_size_x_input = QLineEdit(str(self.default_world_size_x))
        layout.addWidget(self.world_size_x_label, 0, 0)
        layout.addWidget(self.world_size_x_input, 0, 1)

        # World Size Y input
        self.world_size_y_label = QLabel('World Size Y:')
        self.world_size_y_input = QLineEdit(str(self.default_world_size_y))
        layout.addWidget(self.world_size_y_label, 1, 0)
        layout.addWidget(self.world_size_y_input, 1, 1)

        # Organisms Count input
        self.organisms_count_label = QLabel('Count of Organisms:')
        self.organisms_count_input = QLineEdit(str(self.default_organisms_count))
        layout.addWidget(self.organisms_count_label, 2, 0)
        layout.addWidget(self.organisms_count_input, 2, 1)

        # Submit Button
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.createWorld)
        layout.addWidget(self.submit_button, 3, 0, 1, 2)

        # Set the window properties
        self.setWindowTitle('World Simulation Game')
        self.setGeometry(100, 100, 400, 300)
        self.show()

    def clearLayout(self):
        layout = self.central_widget.layout()
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def createWorldGrid(self, world_size_x, world_size_y):
        world_size_x = int(world_size_x)
        world_size_y = int(world_size_y)

        # Create the grid
        grid = self.central_widget.layout()
        grid.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        grid.setContentsMargins(10, 0, 0, 0)
        grid.setSpacing(0)
        # set the margin of the grid layout for the 

        for i in range(world_size_x):
            for j in range(world_size_y):
                button = QPushButton()
                button.setFixedSize(20, 20)
                button.setStyleSheet('''
                    QPushButton {
                        background-color: #333333;
                        border: 1px solid #A917C6;
                        border-radius: 0px;
                        color: #b1b1b1;
                    }
                    QPushButton:hover {
                        background-color: #4A4949;
                    }
                    QPushButton:pressed {
                        background-color: #5A5A5A;
                    }
                ''')
                grid.addWidget(button, i + 4, j)

    def createWorld(self):
        world_size_x = self.world_size_x_input.text()
        world_size_y = self.world_size_y_input.text()
        organisms_count = self.organisms_count_input.text()

        self.clearLayout()
        print('Creating the world...')
        print(f'World Size: {world_size_x} x {world_size_y}')
        print(f'Count of Organisms: {organisms_count}')

        # Create the world
        self.createWorldGrid(world_size_x, world_size_y)

if __name__ == '__main__':
    # clear the console
    os.system('cls' if os.name == 'nt' else 'clear')
    app = QApplication(sys.argv)
    ex = App()
    app.setStyleSheet("""
        QWidget {
            background-color: #2b2b2b;
            color: #b1b1b1;
        }
        QPushButton {
            background-color: #333333;
            border: 1px solid #4A4949;
            border-radius: 2px;
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
    """)
    sys.exit(app.exec())
