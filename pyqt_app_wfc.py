# import random
# import sys
# from PyQt6.QtWidgets import QApplication
# from PyQt6.QtWidgets import QGridLayout
# from PyQt6.QtWidgets import QHBoxLayout
# from PyQt6.QtWidgets import QPushButton
# from PyQt6.QtWidgets import QWidget
# COLOR_POOL = ["red", "green", "blue", "yellow", "purple", "orange"]
# class ColorTilesApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Color Tiles with Ctrl Click (PyQt6)")
#         # Layout
#         self.layout = QGridLayout()
#         # self.layout.setContentsMargins(0,0,0,0)
#         self.layout.setSpacing(0)
#         self.setLayout(self.layout)
#         # Tiles buttons
#         self.width = 5
#         self.height = 2
#         self.tiles = [[] for x in range(self.height)]
#         # Random initial colors for all.
#         self.colors = [
#             random.sample(COLOR_POOL, self.width) for _ in range(self.height)
#         ]
#         for i in range(self.height):
#             for j in range(self.width):
#                 btn = QPushButton("")
#                 btn.setFixedSize(100, 200)
#                 color = self.colors[i][j]
#                 # color = random.choice(COLOR_POOL)
#                 btn.setStyleSheet(  # This is some chatgpt magic for setting the color.
#                     f"background-color: {color}; border: 0px solid black;"
#                 )
#                 # btn.setStyleSheet( # This is some chatgpt magic for setting the color.
#                 #     f"background-color: {color}; border: 2px solid black;"
#                 # )
#                 # This is where we define what arguments to give to the "handle click" function. (i,j) as input is defined here.
#                 btn.clicked.connect(
#                     lambda checked, index=(i, j): self.handle_click(index)
#                 )
#                 self.tiles[i].append(btn)
#                 self.layout.addWidget(btn, i, j)
#     def handle_click(self, index):
#         i, j = index[0], index[1]
#         current_color = self.colors[i][j]
#         new_color = random.choice([c for c in COLOR_POOL if c != current_color])
#         self.colors[i][j] = new_color
#         self.update_colors()
#     def update_colors(self):
#         for i in range(self.height):
#             for j in range(self.width):
#                 color = self.colors[i][j]
#                 btn = self.tiles[i][j]
#                 # btn.setStyleSheet(
#                 #     f"background-color: {color}; border: 2px solid black;"
#                 # )
#                 btn.setStyleSheet(
#                     f"background-color: {color}; border: 0px solid black;"
#                 )
# def main():
#     app = QApplication(sys.argv)
#     window = ColorTilesApp()
#     window.show()
#     sys.exit(app.exec())
# if __name__ == "__main__":
#     main()
import random
import sys
from functools import partial

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QWidget

COLOR_POOL = ["red", "green", "blue", "yellow", "purple", "orange"]


class ColorTilesApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Color Tiles with Ctrl Click (PyQt6)")

        # Layout
        self.layout = QGridLayout()
        # self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        # Tiles buttons

        self.width = 5
        self.height = 2

        self.tiles = [[] for x in range(self.height)]

        # Random initial colors for all.
        self.colors = [
            random.sample(COLOR_POOL, self.width) for _ in range(self.height)
        ]

        for i in range(self.height):
            for j in range(self.width):

                btn = QPushButton("")
                btn.setFixedSize(100, 200)
                color = self.colors[i][j]
                # color = random.choice(COLOR_POOL)
                btn.setStyleSheet(  # This is some chatgpt magic for setting the color.
                    f"background-color: {color}; border: 0px solid black;"
                )
                # btn.setStyleSheet( # This is some chatgpt magic for setting the color.
                #     f"background-color: {color}; border: 2px solid black;"
                # )
                # This is where we define what arguments to give to the "handle click" function. (i,j) as input is defined here.
                btn.clicked.connect(partial(self.handle_click, btn))
                self.tiles[i].append(btn)
                self.layout.addWidget(btn, i, j)

    def handle_click(self, btn):

        new_color = random.choice([c for c in COLOR_POOL])
        btn.setStyleSheet(  # This is some chatgpt magic for setting the color.
            f"background-color: {new_color}; border: 0px solid black;"
        )


def main():
    app = QApplication(sys.argv)
    window = ColorTilesApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
