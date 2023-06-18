import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


def flatten_list_of_lists(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]


def plot_landscape(landscape, characters):

    char_list = list(
        characters.keys()
    )  # Position in this is value, We do this once so the value is locked for each tile
    char_dict = {c: i for i, c in enumerate(char_list)}  # tile: value
    values = np.vectorize(char_dict.get)(landscape)
    colors = np.array([characters[char_list[i]] for i, c in enumerate(char_list)])
    cmap = ListedColormap(colors)
    fig, ax = plt.subplots()

    cax = ax.imshow(values, cmap, rasterized=True, vmin=0, vmax=len(characters))
    cbar = fig.colorbar(cax, cmap=cmap, ticks=np.arange(0, len(characters)) + 0.5)
    cbar.ax.set_yticklabels(char_list)
    return fig, ax
