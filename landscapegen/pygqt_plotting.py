import math
import random
import sys
from functools import partial

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QBrush
from PyQt6.QtGui import QColor
from PyQt6.QtGui import QPainter
from PyQt6.QtGui import QPalette
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget

from landscapegen.tileset import Tileset_wfc
from landscapegen.wavefunction import collapse
from landscapegen.wavefunction import get_flat_coords_of_undetermined
from landscapegen.wavefunction import get_only_tile
from landscapegen.wavefunction import get_tile_option_list
from landscapegen.wavefunction import Wavefunction


class ColorTilesApp(QWidget):
    """Main logic: make a widget that plots a nxm grid.
    If its determined, plot a solid color/representation.
    If its undetermined, plot a smaller square grid(2x2, 3x3,4x4 etc) of all the options.
    When a button is clicked, choose the corresponding tile in the wavefunction, collapsing that cell.
    After collapse, redraw the tiles.
    """

    def __init__(self, wavefunction: Wavefunction, tileset: Tileset_wfc):
        super().__init__()
        self.setWindowTitle("Color Tiles with Ctrl Click (PyQt6)")
        # consts
        self.major_pixels = 60  # Number of pixels in a major cell

        # Layout(main)
        self.layout_main = QVBoxLayout()
        # self.main_layout.setSpacing(0)
        # self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Layout(buttons)
        self.layout_panel = QVBoxLayout()
        # Collapse once
        btn_collapse = QPushButton("Collapse!")
        btn_collapse.clicked.connect(partial(self.collapse_cell, i=None, j=None, chosen=None))
        self.layout_panel.addWidget(btn_collapse)

        # Play timer
        self.timer = QTimer()
        self.timer.setInterval(300)  # in milliseconds
        self.timer.timeout.connect(self.collapse_cell)

        # Play
        btn_play = QPushButton("Play!")
        btn_play.clicked.connect(self.btn_func_play)
        self.layout_panel.addWidget(btn_play)

        # Pause
        btn_pause = QPushButton("Pause!")
        btn_pause.clicked.connect(partial(self.btn_func_pause))
        self.layout_panel.addWidget(btn_pause)

        # save
        btn_save = QPushButton("Save")
        btn_save.clicked.connect(self.btn_func_save)
        self.layout_panel.addWidget(btn_save)

        # Layout(wfc)
        self.layout_wfc = QGridLayout()
        self.layout_wfc.setContentsMargins(0, 0, 0, 0)
        self.layout_wfc.setSpacing(0)

        # Layout(main)
        self.layout_main.addLayout(self.layout_panel)
        self.layout_main.addLayout(self.layout_wfc)
        self.setLayout(self.layout_main)

        # Tiles buttons
        self.wavefunction = wavefunction
        self.tileset = tileset
        self.width = self.wavefunction.width
        self.height = self.wavefunction.height
        self.play = False
        self.cell_widgets = [[None for _ in range(self.width)] for _ in range(self.height)]

        # Calculate minor gridsize struff
        # nxn gridsize in smaller grid.
        self.minor_gridsize = math.ceil(math.sqrt(len(self.tileset.info)))
        self.minor_pixels = int(self.major_pixels / self.minor_gridsize)

        # More difficult calculations
        self.invalid_choice_pixmap = self.checkerboard_pixmap(pixels=self.minor_pixels)
        self.dict_reserved = self.make_dict_reserved()

        for i in range(self.height):
            for j in range(self.width):
                cell = self.wavefunction.wf[i][j]
                # We have to determine this cells content. Either its determined or undetermined. We add a widget to the square no matter what.
                # 2 cases:
                if len(cell) == 1:
                    # This cell is already determined, just plot it, with no button action.
                    widget = self.make_determined_widget(get_only_tile(cell))
                else:
                    # This cell is not determined! We need to plot all possibilities.
                    widget = QWidget()  # Add the container widget
                    small_layout = QGridLayout(widget)  # Make a smaller layout here.
                    small_layout.setSpacing(0)
                    small_layout.setContentsMargins(0, 0, 0, 0)
                    widget.setFixedSize(self.major_pixels, self.major_pixels)

                    # TODO: save computation here by making the print once(all black) and removing/adding what is needed.
                    for small_i in range(self.minor_gridsize):
                        for small_j in range(self.minor_gridsize):
                            btn = QPushButton()
                            btn.setFixedSize(self.minor_pixels, self.minor_pixels)

                            if (small_i, small_j) in self.dict_reserved and self.dict_reserved[
                                (small_i, small_j)
                            ] in cell:  # This tile is reserved, so the order is consistent. Paint the reserved tile
                                chosen_tile = self.dict_reserved[(small_i, small_j)]
                                rgba = [int(c * 255) for c in self.tileset.info[chosen_tile]]
                                # Chosen thing in cell [i,j]
                                # Partial is some magic to connect the button to a function and add arguments
                                btn.clicked.connect(partial(self.collapse_cell, i, j, chosen_tile))
                                btn.setStyleSheet(f"background-color: rgba{tuple(rgba)}; border: 0px solid black;")
                            else:  # This cell is either not reserved for a specific tile, or the specific tile is not possible any more. So we paint the "invalid choice" tile.
                                palette = btn.palette()
                                palette.setBrush(QPalette.ColorRole.Button, QBrush(self.invalid_choice_pixmap))
                                btn.setAutoFillBackground(True)
                                btn.setPalette(palette)

                            small_layout.addWidget(btn, small_i, small_j)

                self.cell_widgets[i][j] = widget
                self.layout_wfc.addWidget(widget, i, j)

    def collapse_cell(self, i: int = None, j: int = None, chosen: str = None):
        """Collapse a cell with the given choice.

        Args:
            i (int): "height" from top of canvas
            j (int): "width" from left of canvas
            chosen (str): The chosen tile for this cell.
        """
        wf = self.wavefunction.wf
        collapse_random = i is None and j is None and chosen is None  # No selection -> must be random
        if collapse_random:
            flat_coords = get_flat_coords_of_undetermined(wavefunction=wf)
            if len(flat_coords) == 0:  # If the timer is going and there is no more to choose, stop the timer.
                print("nothing more to collapse!")
                self.play = False
                self.timer.stop()
                return
            point = random.choice(flat_coords)  # Random point to collapse

            cell = wf[point[0]][point[1]]
            chosen = random.choice(get_tile_option_list(cell))
        else:
            print(i, j, chosen)
            point = (i, j)
        forbidden = set(wf[point[0]][point[1]]) - set([chosen])

        collapse(point=point, remove_in=forbidden, wavefunction=wf, tileset=self.tileset)
        self.wavefunction = Wavefunction(wf)

        # Find out which cells are affected and re-render these.
        affected = []
        for i in range(self.height):
            for j in range(self.width):
                affected.append([i, j])
        for x, y in affected:
            self.render_cell(x, y)

    def btn_func_play(self):
        self.play = True
        self.timer.start()

    def btn_func_pause(self):
        self.play = False
        self.timer.stop()

    def btn_func_save(self):
        self.wavefunction.save("wf.txt")

    def render_cell(self, i: int, j: int):
        """Renders the cell. This should be called after there is a change to a cell.

        Args:
            i (int): "height" from top of canvas
            j (int): "width" from left of canvas
        """
        cell = self.wavefunction.wf[i][j]

        # Remove old widget
        old = self.cell_widgets[i][j]
        if old:
            self.layout_wfc.removeWidget(old)
            old.deleteLater()

        if len(cell) == 1:
            # This cell is already determined, just plot it, with no button action.
            widget = self.make_determined_widget(get_only_tile(cell))

        else:
            widget = QWidget()
            layout = QGridLayout(widget)
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)
            widget.setFixedSize(self.major_pixels, self.major_pixels)

            idx = 0
            for small_i in range(self.minor_gridsize):
                for small_j in range(self.minor_gridsize):
                    btn = QPushButton()
                    btn.setFixedSize(self.minor_pixels, self.minor_pixels)

                    if (small_i, small_j) in self.dict_reserved and self.dict_reserved[(small_i, small_j)] in cell:
                        chosen_tile = self.dict_reserved[(small_i, small_j)]
                        rgba = [int(c * 255) for c in self.tileset.info[chosen_tile]]
                        btn.clicked.connect(partial(self.collapse_cell, i, j, chosen_tile))
                        btn.setStyleSheet(f"background-color: rgba{tuple(rgba)}; border: 0px;")
                    else:
                        palette = btn.palette()
                        palette.setBrush(QPalette.ColorRole.Button, QBrush(self.invalid_choice_pixmap))
                        btn.setAutoFillBackground(True)
                        btn.setPalette(palette)

                    layout.addWidget(btn, small_i, small_j)
                    idx += 1

        self.cell_widgets[i][j] = widget
        self.layout_wfc.addWidget(widget, i, j)

    def make_dict_reserved(self) -> dict[tuple[int, int], str]:
        """Figure out which tile should be reserved in which coordinates (i,j).

        Returns:
            dict[tuple[int,int], str]: (i,j) coord of which coordinates go to which tile.
        """
        dict_reserved = {}
        for t, tile in enumerate(self.tileset.info):  # for each tile type.
            j_coord = t % self.minor_gridsize  # get height coord
            i_coord = math.floor(t / self.minor_gridsize)  # get width coord.
            dict_reserved[(i_coord, j_coord)] = tile

        return dict_reserved

    def checkerboard_pixmap(self, pixels: int, tile: int = None) -> QPixmap:
        """Generate the pixmap used to mark tiles taht cannot be chosen/clicked.
        Its a checkered board of grey and pink.

        Args:
            pixels (int): Pixel size of the whole checkerboard, should be the exact size of a tile in the smaller grid.
            tile (int, optional): Size of each complete grey or pink tile in the checkerboard

        Returns:
            QPixmap: Pixmap denoting an unselectable tile.
        """

        tile = tile if tile else int(pixels / 4)
        pixmap = QPixmap(pixels, pixels)
        color_grey = QColor("#ededed")
        color_soft_pink = QColor("#ead1dc")
        pixmap.fill(color_grey)

        painter = QPainter(pixmap)

        for y in range(0, pixels, tile):
            for x in range(0, pixels, tile):
                if (x // tile + y // tile) % 2 == 0:
                    painter.fillRect(x, y, tile, tile, color_soft_pink)

        painter.end()
        return pixmap

    def make_determined_widget(self, tile: str) -> QWidget:
        """Makes the widget for a determined cell.

        Args:
            tile (str): String representation of the determined cell.

        Returns:
            QWidget: Widget ready to plot into the layout.
        """

        widget = QPushButton()
        widget.setFixedSize(self.major_pixels, self.major_pixels)
        rgba = [int(c * 255) for c in self.tileset.info[tile]]
        widget.setStyleSheet(f"background-color: rgba{tuple(rgba)}; border: 0px solid black;")
        return widget


def pyqt_plot(wavefunction: Wavefunction, tileset: Tileset_wfc):
    app = QApplication(sys.argv)
    window = ColorTilesApp(wavefunction=wavefunction, tileset=tileset)
    window.show()
    sys.exit(app.exec())
