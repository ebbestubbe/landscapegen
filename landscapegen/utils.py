import copy
import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


def flatten_list_of_lists(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]


def plot_landscape(landscape, tileset_info):
    size0 = len(landscape)
    size1 = len(landscape[1])
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
    # ax.set_xticks(np.arange(-.5, 10, 1), minor=True)
    # ax.set_yticks(np.arange(-.5, 10, 1), minor=True)
    ax.set_xticks(np.arange(-0.5, size1, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, size0, 1), minor=True)
    ax.grid(which="minor", color="w", linestyle="-", linewidth=2)
    # ax.grid()
    return fig, ax


def plot_incomplete(wavefunction, tileset):

    info = copy.deepcopy(tileset.info)
    info["Void"] = [1, 1, 1, 1]
    info["impossible"] = [1, 0, 1, 1]
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


def get_mini_grid_size(tileset_info):
    n_tiles = len(tileset_info.keys())

    return math.pow(math.ceil(math.sqrt(n_tiles)), 2)


def is_split_required(landscape):
    ...


def plotting_thing():
    ...
    # Split the incoming 3d arrays into a 2d array of 1d arrays.
    # If the array has length 1, plot the plotting matrix should only plot that one thing.
    # If there are more elements in the array, get the "mini_grid_size" of the wavefunction.
    # 2,3,4-> 4
    # 5,...9-> 9
    # etc

    # For each array, if it has length 1, it means the cell has been collapsed,
    # plot that whole grid in that color.
    # If the array is longer, color the first square in one color, then the next
    # in the next color, etc. If any leftover, color with a "void" color.
