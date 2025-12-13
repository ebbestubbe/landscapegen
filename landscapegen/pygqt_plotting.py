import math
import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QWidget

from landscapegen.tileset import Tileset_wfc
from landscapegen.wavefunction import Wavefunction

major_pixels = 48


class ColorTilesApp(QWidget):
    def __init__(self, wavefunction: Wavefunction, tileset: Tileset_wfc):
        super().__init__()
        self.setWindowTitle("Color Tiles with Ctrl Click (PyQt6)")
        # Layout
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        # Tiles buttons

        self.width = wavefunction.width
        self.height = wavefunction.height

        # self.tiles = [[] for x in range(self.height)] #TODO figure out if this is used?

        minor_gridsize = math.ceil(
            math.sqrt(len(tileset.info.keys()))
        )  # nxn gridsize in smaller grid.
        minor_pixels = int(major_pixels / minor_gridsize)
        for i in range(self.height):
            for j in range(self.width):
                cell = wavefunction.wf[i][j]
                if (
                    len(cell) == 1
                ):  # This cell is already determined, just plot it, with no button action.
                    btn = QPushButton("")  # TODO is this emmpty string needwed?
                    btn.setFixedSize(major_pixels, major_pixels)
                    rgba_color = [int(part * 255) for part in tileset.info[cell[0]]]

                    btn.setStyleSheet(
                        f"background-color: rgba{tuple(rgba_color)}; border: 0px solid black;"
                    )

                    # self.tiles[i].append(btn)`#TODO figure out if this is used?`
                    self.layout.addWidget(btn, i, j)
                else:  # This cell is not determined! We need to plot all possibilities.
                    container = QWidget()
                    small_layout = QGridLayout(container)  # Make a smaller layout here.
                    small_layout.setSpacing(0)

                    small_layout.setContentsMargins(0, 0, 0, 0)
                    container.setFixedSize(major_pixels, major_pixels)

                    # TODO: save computation here by making the print once(all black) and removing/adding what is needed.
                    inner_i = 0
                    for small_i in range(minor_gridsize):
                        for small_j in range(minor_gridsize):

                            btn = QPushButton("")
                            btn.setFixedSize(minor_pixels, minor_pixels)
                            if inner_i < len(cell):
                                rgba_color = [
                                    int(part * 255)
                                    for part in tileset.info[cell[inner_i]]
                                ]
                            else:
                                rgba_color = [0, 0, 0, 1]
                            btn.setStyleSheet(
                                f"background-color: rgba{tuple(rgba_color)}; border: 0px solid black;"
                            )
                            small_layout.addWidget(btn, small_i, small_j)
                            inner_i += 1

                    self.layout.addWidget(
                        container, i, j
                    )  # Add the finished layout to the position in the cell.


def pyqt_plot(wavefunction: Wavefunction, tileset: Tileset_wfc):
    app = QApplication(sys.argv)
    window = ColorTilesApp(wavefunction=wavefunction, tileset=tileset)
    window.show()
    sys.exit(app.exec())
