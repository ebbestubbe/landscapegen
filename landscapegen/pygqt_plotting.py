import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QWidget

from landscapegen.tileset import Tileset_wfc
from landscapegen.wavefunction import Wavefunction


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

        for i in range(self.height):
            for j in range(self.width):

                btn = QPushButton("")
                btn.setFixedSize(50, 50)
                rgba_color = [
                    int(part * 255) for part in tileset.info[wavefunction.wf[i][j][0]]
                ]

                btn.setStyleSheet(
                    f"background-color: rgba{tuple(rgba_color)}; border: 0px solid black;"
                )

                self.tiles[i].append(btn)
                self.layout.addWidget(btn, i, j)


def pyqt_plot(wavefunction: Wavefunction, tileset: Tileset_wfc):
    app = QApplication(sys.argv)
    window = ColorTilesApp(wavefunction=wavefunction, tileset=tileset)
    window.show()
    sys.exit(app.exec())
