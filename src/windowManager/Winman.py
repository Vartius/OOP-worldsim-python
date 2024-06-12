from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QGridLayout,
    QHBoxLayout,
    QScrollArea,
    QMessageBox,
    QDialog,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from worldsim.world.World import World
from typing import Union


class WindowManager(QMainWindow):
    def __init__(self, worldManager: "World"):
        super().__init__()
        self.worldManager = worldManager
        self.default_world_size_x: int = 20
        self.default_world_size_y: int = 20
        self.default_organisms_count: int = 20
        self.initUI()

    def initUI(self) -> None:
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        main_layout = QHBoxLayout()
        self.central_widget.setLayout(main_layout)
        self.game_layout = QGridLayout()
        self.logs_layout = QVBoxLayout()
        main_layout.addLayout(self.game_layout)
        main_layout.addLayout(self.logs_layout)
        self.initGameLayout()
        self.setWindowTitle("World Simulation Game")
        self.show()

    def initGameLayout(self) -> None:
        self.game_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.game_layout.setContentsMargins(10, 10, 10, 10)
        # screen_size = self.screen().geometry()
        self.world_size_x_label = QLabel("World Size X:")
        self.world_size_x_input = QLineEdit(str(self.default_world_size_x))
        self.game_layout.addWidget(self.world_size_x_label, 0, 0)
        self.game_layout.addWidget(self.world_size_x_input, 0, 1)
        self.world_size_y_label = QLabel("World Size Y:")
        self.world_size_y_input = QLineEdit(str(self.default_world_size_y))
        self.game_layout.addWidget(self.world_size_y_label, 1, 0)
        self.game_layout.addWidget(self.world_size_y_input, 1, 1)
        self.organisms_count_label = QLabel("Count of Organisms:")
        self.organisms_count_input = QLineEdit(str(self.default_organisms_count))
        self.game_layout.addWidget(self.organisms_count_label, 2, 0)
        self.game_layout.addWidget(self.organisms_count_input, 2, 1)
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.createWorld)
        self.game_layout.addWidget(self.submit_button, 3, 0, 1, 2)

    def clearLayout(self, layout: Union[QGridLayout, QHBoxLayout, QVBoxLayout]) -> None:
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget:
                    widget.deleteLater()

    def addLogsOnLayout(self) -> None:
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        self.logs_layout.addWidget(QLabel("Logs:"))
        self.logs_layout.addWidget(self.scroll_area)
        self.logs = QLabel("Start of logs...")
        self.scroll_layout.addWidget(self.logs)

    def addOrganismButton(self, i: int, j: int, text: str):
        return lambda: self.worldManager.addOrganismByDraw(i, j, text)

    def gridButtonClicked(self, i: int, j: int) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle("Organism Info")
        dialog_layout = QVBoxLayout()
        dialog.setLayout(dialog_layout)
        org = self.worldManager.getOrganismAt(i, j)
        if org is not None:
            label = QLabel(f"Organism at ({i}, {j}): {org.getName()}")
            dialog_layout.addWidget(label)
            label = QLabel(f"Strength: {org.getStrength()}")
            dialog_layout.addWidget(label)
            label = QLabel(f"Initiative: {org.getInitiative()}")
            dialog_layout.addWidget(label)
            label = QLabel(f"Spawn Age: {org.getSpawnAge()}")
            dialog_layout.addWidget(label)
            label = QLabel(f"Alive: {org.getAlive()}")
            dialog_layout.addWidget(label)
        else:
            label = QLabel(f"No organism at ({i}, {j})")
            dialog_layout.addWidget(label)

        d = {
            "Antelope": "A",
            "Fox": "F",
            "Sheep": "S",
            "Turtle": "T",
            "Wolf": "W",
            "Grass": "G",
            "Guarana": "U",
            "Hogweed": "O",
            "DeadlyNightshade": "D",
        }
        for k in d:
            button = QPushButton(k)
            button.clicked.connect(self.addOrganismButton(i, j, d[k]))
            dialog_layout.addWidget(button)
        button = QPushButton("Close")
        button.clicked.connect(dialog.close)
        dialog_layout.addWidget(button)
        dialog.exec()

    def createButtonCallback(self, i: int, j: int):
        return lambda: self.gridButtonClicked(i, j)

    def createWorldGrid(self, world_size_x: int, world_size_y: int) -> None:
        world_size_x = int(world_size_x)
        world_size_y = int(world_size_y)
        self.game_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.game_layout.setContentsMargins(10, 0, 0, 0)
        self.game_layout.setSpacing(0)
        self.buttons = []
        for i in range(world_size_x):
            row_buttons = []
            for j in range(world_size_y):
                button = QPushButton()
                button.clicked.connect(self.createButtonCallback(i, j))
                size = int(min(700 / world_size_x, 700 / world_size_y))
                button.setFixedSize(size, size)
                button.setStyleSheet(
                    """
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
                """
                )
                self.game_layout.addWidget(button, i + 4, j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)
        self.addLogsOnLayout()

    def createWorld(self) -> None:
        self.world_size_x = int(self.world_size_x_input.text())
        self.world_size_y = int(self.world_size_y_input.text())
        self.organisms_count = self.organisms_count_input.text()
        self.clearLayout(self.game_layout)
        self.createWorldGrid(self.world_size_x, self.world_size_y)
        self.worldManager.initWorld(
            self.getWorldSizeX(), self.getWorldSizeY(), self.getOrganismsCount()
        )

    def addLog(self, log: str) -> None:
        self.logs.setText(f"{self.logs.text()}\n{log}")
        scroll_bar = self.scroll_area.verticalScrollBar()
        if scroll_bar is not None:
            scroll_bar.setValue(scroll_bar.maximum())

    def getWorldSizeX(self) -> int:
        return int(self.world_size_x)

    def getWorldSizeY(self) -> int:
        return int(self.world_size_y)

    def getOrganismsCount(self) -> int:
        return int(self.organisms_count)

    def updateButton(self, i: int, j: int, text: str) -> None:
        self.buttons[i][j].setText(text)

    def updateButtons(self) -> None:
        for i in range(self.getWorldSizeX()):
            for j in range(self.getWorldSizeY()):
                org = self.worldManager.getOrganismAt(i, j)
                if org is not None:
                    self.updateButton(i, j, org.draw())
                else:
                    self.updateButton(i, j, "")

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key_map = {
            Qt.Key.Key_W: "W",
            Qt.Key.Key_A: "A",
            Qt.Key.Key_S: "S",
            Qt.Key.Key_D: "D",
            Qt.Key.Key_E: "E",
            Qt.Key.Key_Q: "Q",
            Qt.Key.Key_Y: "Y",
            Qt.Key.Key_L: "L",
        }
        if self.worldManager.human_turn:
            key = event.key()
            if key in key_map:
                self.worldManager.handleHumanMove(key_map[key])
            else:
                super().keyPressEvent(event)

    def enableHumanControls(self) -> None:
        self.setFocus()

    def closeGame(self) -> None:
        self.close()

    def restartGame(self) -> None:
        self.clearLayout(self.game_layout)
        self.clearLayout(self.logs_layout)
        self.worldManager.clearOrganisms()
        self.initGameLayout()

    def gameOver(self, msg) -> None:
        # game over message
        self.addLog("Game Over!")
        # dialog
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setText("Game Over - " + msg + "!")
        msgBox.setInformativeText("Do you want to restart the game or exit?")
        msgBox.setWindowTitle("Game Over")
        msgBox.setStandardButtons(
            QMessageBox.StandardButton.Retry | QMessageBox.StandardButton.Close
        )

        ret = msgBox.exec()

        if ret == QMessageBox.StandardButton.Retry:
            self.restartGame()
        elif ret == QMessageBox.StandardButton.Close:
            self.closeGame()

    def resetGame(self, data: dict) -> None:
        self.clearLayout(self.game_layout)
        self.clearLayout(self.logs_layout)
        self.world_size_x = data["world_size_x"]
        self.world_size_y = data["world_size_y"]
        self.organisms_count = data["organisms_count"]
        self.createWorldGrid(self.world_size_x, self.world_size_y)
        self.updateButtons()
        self.setLogs(data["logs"])

    def getLogs(self) -> str:
        return self.logs.text()

    def setLogs(self, logs: str) -> None:
        self.logs.setText(logs)
