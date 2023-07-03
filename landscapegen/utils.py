import copy

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


def flatten_list_of_lists(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]


def plot_landscape(landscape, tileset_info):

    char_list = list(
        tileset_info.keys()
    )  # Position in this is value, We do this once so the value is locked for each tile
    char_dict = {c: i for i, c in enumerate(char_list)}  # tile: value
    values = np.vectorize(char_dict.get)(landscape)
    colors = np.array([tileset_info[char_list[i]] for i, c in enumerate(char_list)])
    cmap = ListedColormap(colors)
    fig, ax = plt.subplots()

    cax = ax.imshow(values, cmap, rasterized=True, vmin=0, vmax=len(tileset_info))
    cbar = fig.colorbar(cax, cmap=cmap, ticks=np.arange(0, len(tileset_info)) + 0.5)
    cbar.ax.set_yticklabels(char_list)
    return fig, ax


def plot_incomplete(wavefunction):

    info = {
        "Grass": [0, 1, 0, 1],
        "Water": [0, 0, 1, 1],
        "Sand": [1, 1, 0, 1],
        "Void": [0, 0, 0, 1],
        "Cliff": [0, 0, 0, 1],
        "Lava": [1, 0, 0, 1],
        "impossible": [1, 0, 1, 1],
    }
    wavefunc2 = copy.deepcopy(wavefunction)
    size0 = len(wavefunc2)
    size1 = len(wavefunc2[0])
    for jj in range(size0):
        for ii in range(size1):
            cell = wavefunc2[jj][ii]
            # if len(cell) == 1:
            # print(f"{jj}, {ii} is {cell}")
            if len(cell) == 0:
                wavefunc2[jj][ii] = ["Void"]
                # print(f"{jj}, {ii} is void")
            if len(cell) > 1:
                wavefunc2[jj][ii] = ["impossible"]
                # print(f"{jj}, {ii} is impossible")
    landscape = np.array(wavefunc2)
    plot_landscape(landscape=landscape, tileset_info=info)
    print("foo")
