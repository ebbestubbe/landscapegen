import random
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QWidget

COLOR_POOL = ["red", "green", "blue", "yellow", "purple", "orange"]


class ColorTilesApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Color Tiles with Ctrl Click (PyQt6)")

        # Initial colors for 4 tiles
        self.colors = ["red", "green", "blue", "yellow"]

        # Layout
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Tiles buttons
        self.tiles = []
        for i in range(4):
            btn = QPushButton("")
            btn.setFixedSize(100, 100)
            btn.setStyleSheet(
                f"background-color: {self.colors[i]}; border: 2px solid black;"
            )
            btn.clicked.connect(lambda checked, index=i: self.handle_click(index))
            self.tiles.append(btn)
            self.layout.addWidget(btn)

        # Black mode checkbox (alternative to Ctrl for desktop app)
        self.black_mode_checkbox = QCheckBox("Black Mode (Ctrl-click also sets black)")
        self.black_mode_checkbox.setChecked(False)
        self.layout.addWidget(self.black_mode_checkbox)

        # Timer for auto-changing tile (index 3)
        self.timer = QTimer()
        self.timer.setInterval(1000)  # 1 second
        self.timer.timeout.connect(self.auto_change_tile)
        self.timer.start()

    def handle_click(self, index):
        # Detect if Ctrl is pressed during click
        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = modifiers & Qt.KeyboardModifier.ControlModifier

        if ctrl_pressed:
            self.colors[index] = "black"
        else:
            if index == 3:
                # Tile 4 is auto-changing only, ignore clicks or just change color normally
                # Here let's just do nothing or you could change color normally:
                pass
            else:
                current_color = self.colors[index]
                new_color = random.choice([c for c in COLOR_POOL if c != current_color])
                self.colors[index] = new_color

        self.update_colors()

    def auto_change_tile(self):
        # Only tile index 3 auto-changes color every second
        current_color = self.colors[3]
        new_color = random.choice([c for c in COLOR_POOL if c != current_color])
        self.colors[3] = new_color
        self.update_colors()

    def update_colors(self):
        for i, btn in enumerate(self.tiles):
            # If black mode checkbox is checked AND tile is clicked, always show black (except auto tile)
            if (
                self.black_mode_checkbox.isChecked()
                and i != 3
                and self.colors[i] != "black"
            ):
                # If black mode active, force color to black (like Ctrl)
                btn.setStyleSheet("background-color: black; border: 2px solid black;")
            else:
                btn.setStyleSheet(
                    f"background-color: {self.colors[i]}; border: 2px solid black;"
                )


def main():
    app = QApplication(sys.argv)
    window = ColorTilesApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
