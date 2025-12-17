import math
import sys
from functools import partial

from PyQt6.QtGui import QBrush
from PyQt6.QtGui import QColor
from PyQt6.QtGui import QPainter
from PyQt6.QtGui import QPalette
from PyQt6.QtGui import QPixmap
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

        self.cell_widgets = [
            [None for _ in range(self.width)] for _ in range(self.height)
        ]

        # self.tiles = [[] for x in range(self.height)] #TODO figure out if this is used?

        minor_gridsize = math.ceil(
            math.sqrt(len(self.tileset.info.keys()))
        )  # nxn gridsize in smaller grid.
        minor_pixels = int(major_pixels / minor_gridsize)

        self.invalid_choice_pixmap = self.checkerboard_pixmap(pixels=minor_pixels)

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

                    self.cell_widgets[i][j] = btn
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
                                btn.setStyleSheet(
                                    f"background-color: rgba{tuple(rgba_color)}; border: 0px solid black;"
                                )
                            else:
                                palette = btn.palette()
                                palette.setBrush(
                                    QPalette.ColorRole.Button,
                                    QBrush(self.invalid_choice_pixmap),
                                )
                                btn.setAutoFillBackground(True)
                                btn.setPalette(palette)

                            small_layout.addWidget(btn, small_i, small_j)
                            inner_i += 1

                    self.cell_widgets[i][j] = container
                    self.layout.addWidget(
                        container, i, j
                    )  # Add the finished layout to the position in the cell.

    def checkerboard_pixmap(self, pixels=40, tile=10):
        # Generate the pixmap used to mark tiles taht cannot be chosen/clicked.
        # TODO: Maybe this should be a png instead?
        pixmap = QPixmap(pixels, pixels)
        color_gray = QColor("#ededed")
        color_soft_pink = QColor("#ead1dc")
        pixmap.fill(color_gray)

        painter = QPainter(pixmap)

        for y in range(0, pixels, tile):
            for x in range(0, pixels, tile):
                if (x // tile + y // tile) % 2 == 0:
                    painter.fillRect(x, y, tile, tile, color_soft_pink)

        painter.end()
        return pixmap

    def collapse_cell(self, i, j, chosen):
        print(i, j, chosen)
        point = (i, j)
        wf = self.wavefunction.wf
        remove_in = set(wf[i][j]) - set([chosen])

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
        affected = []
        for i in range(self.height):
            for j in range(self.width):
                affected.append([i, j])
        for (x, y) in affected:
            self.render_cell(x, y)

    def render_cell(self, i, j):
        cell = self.wavefunction.wf[i][j]

        # Remove old widget
        old = self.cell_widgets[i][j]
        if old:
            self.layout.removeWidget(old)
            old.deleteLater()

        if len(cell) == 1:
            btn = QPushButton("")
            btn.setFixedSize(major_pixels, major_pixels)
            rgba = [int(c * 255) for c in self.tileset.info[cell[0]]]
            btn.setStyleSheet(f"background-color: rgba{tuple(rgba)}; border: 0px;")
            widget = btn
        else:
            widget = QWidget()
            layout = QGridLayout(widget)
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)
            widget.setFixedSize(major_pixels, major_pixels)

            minor_gridsize = math.ceil(math.sqrt(len(self.tileset.info)))
            minor_pixels = major_pixels // minor_gridsize

            idx = 0
            for x in range(minor_gridsize):
                for y in range(minor_gridsize):
                    btn = QPushButton("")
                    btn.setFixedSize(minor_pixels, minor_pixels)

                    if idx < len(cell):
                        tile = cell[idx]
                        rgba = [int(c * 255) for c in self.tileset.info[tile]]
                        btn.clicked.connect(partial(self.collapse_cell, i, j, tile))
                        btn.setStyleSheet(
                            f"background-color: rgba{tuple(rgba)}; border: 0px;"
                        )
                    else:
                        palette = btn.palette()
                        palette.setBrush(
                            QPalette.ColorRole.Button,
                            QBrush(self.invalid_choice_pixmap),
                        )
                        btn.setAutoFillBackground(True)
                        btn.setPalette(palette)

                    layout.addWidget(btn, x, y)
                    idx += 1

        self.cell_widgets[i][j] = widget
        self.layout.addWidget(widget, i, j)


def pyqt_plot(wavefunction: Wavefunction, tileset: Tileset_wfc):
    app = QApplication(sys.argv)
    window = ColorTilesApp(wavefunction=wavefunction, tileset=tileset)
    window.show()
    sys.exit(app.exec())
