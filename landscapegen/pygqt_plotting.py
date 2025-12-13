import math
import sys
from functools import partial

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QWidget

from landscapegen.tileset import Tileset_wfc
from landscapegen.wavefunction import collapse
from landscapegen.wavefunction import Wavefunction


major_pixels = 60


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
        self.wavefunction = wavefunction
        self.tileset = tileset
        self.width = self.wavefunction.width
        self.height = self.wavefunction.height

        # self.tiles = [[] for x in range(self.height)] #TODO figure out if this is used?

        minor_gridsize = math.ceil(
            math.sqrt(len(self.tileset.info.keys()))
        )  # nxn gridsize in smaller grid.
        minor_pixels = int(major_pixels / minor_gridsize)
        for i in range(self.height):
            for j in range(self.width):
                cell = self.wavefunction.wf[i][j]
                if (
                    len(cell) == 1
                ):  # This cell is already determined, just plot it, with no button action.
                    btn = QPushButton("")  # TODO is this emmpty string needwed?
                    btn.setFixedSize(major_pixels, major_pixels)
                    rgba_color = [
                        int(part * 255) for part in self.tileset.info[cell[0]]
                    ]

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
                                chosen = cell[inner_i]
                                rgba_color = [
                                    int(part * 255)
                                    for part in self.tileset.info[chosen]
                                ]
                                # Chosen thing in cell [i,j]
                                btn.clicked.connect(
                                    partial(self.collapse_cell, i, j, chosen)
                                )
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

    def collapse_cell(self, i, j, chosen):
        print(i, j, chosen)
        point = (i, j)
        wf = self.wavefunction.wf
        remove_in = set(wf[point[0]][point[1]]) - set([chosen])

        collapse(
            point=point,
            remove_in=remove_in,
            wavefunction=wf,
            tileset=self.tileset,
            width=self.width,
            height=self.height,
        )
        self.wavefunction = Wavefunction(wf)
        print(self.wavefunction)


def pyqt_plot(wavefunction: Wavefunction, tileset: Tileset_wfc):
    app = QApplication(sys.argv)
    window = ColorTilesApp(wavefunction=wavefunction, tileset=tileset)
    window.show()
    sys.exit(app.exec())
