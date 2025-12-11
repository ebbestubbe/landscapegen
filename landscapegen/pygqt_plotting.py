import random
import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QWidget

from landscapegen.tileset import Tileset_wfc
from landscapegen.wavefunction import Wavefunction

color_dict = {
    "Grass": "green",
    "Sand": "yellow",
    "Water": "blue",
    "Cliff": "black",
    "Lava": "red",
}


class ColorTilesApp(QWidget):
    def __init__(self, wavefunction: Wavefunction, tileset: Tileset_wfc):
        super().__init__()
        self.setWindowTitle("Color Tiles with Ctrl Click (PyQt6)")
        # Layout
        self.layout = QGridLayout()
        # self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        # Tiles buttons

        self.width = wavefunction.width
        self.height = wavefunction.height

        self.tiles = [[] for x in range(self.height)]

        self.colors = [
            [color_dict[wavefunction.wf[h][w][0]] for w in range(self.width)]
            for h in range(self.height)
        ]
        for i in range(self.height):
            for j in range(self.width):

                btn = QPushButton("")
                btn.setFixedSize(100, 100)
                color = self.colors[i][j]
                # color = random.choice(COLOR_POOL)
                btn.setStyleSheet(  # This is some chatgpt magic for setting the color.
                    f"background-color: {color}; border: 0px solid black;"
                )
                # btn.setStyleSheet( # This is some chatgpt magic for setting the color.
                #     f"background-color: {color}; border: 2px solid black;"
                # )
                # This is where we define what arguments to give to the "handle click" function. (i,j) as input is defined here.
                # btn.clicked.connect(
                #     lambda checked, index=(i, j): self.handle_click(index)
                # )
                self.tiles[i].append(btn)
                self.layout.addWidget(btn, i, j)


def pyqt_plot(wavefunction: Wavefunction, tileset: Tileset_wfc):
    app = QApplication(sys.argv)
    window = ColorTilesApp(wavefunction=wavefunction, tileset=tileset)
    window.show()
    sys.exit(app.exec())
