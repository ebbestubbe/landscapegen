import copy
import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from landscapegen.tileset import Tileset_wfc
from landscapegen.wavefunction import Wavefunction
#from typing import deprecated

def flatten_list_of_lists(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]

#@deprecated("Use plotting_thing")
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

#@deprecated("Use plotting_thing")
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
    # Given a tileset info, returns the smallest square number bigger than the
    # number of different tile types.
    n_tiles = len(tileset_info.keys())

    #return math.pow(math.ceil(math.sqrt(n_tiles)), 2)
    return math.ceil(math.sqrt(n_tiles))


def plotting_thing_landscape(wavefunction, tileset):
    char_dict = {c: i for i, c in enumerate(tileset.characters)}  # tile: value
    
    # Issue is that now the wavefunction might also contain "__BLANK__"  contains 1 more color than tileset.characters,
    # so the -1 gets interpreted as the closest value(0)
    contains_blank = False
    if contains_blank:
        #char_dict.update({"__BLANK__": -1})
        char_dict = {"__BLANK__": -1, **char_dict}
        
        tileset_characters = copy.deepcopy(tileset.characters)
        tileset_characters.insert(0, "__BLANK__")
        tileset_info = copy.deepcopy(tileset.info)
        #tileset_info.update({"__BLANK__": [1,0,1,1]})
        tileset_info = {"__BLANK__": [1,0,1,1], **tileset_info}
        # Uh maybe add to the end instead of top?
    else:
        tileset_characters = tileset.characters
        tileset_info = tileset.info
    colors = np.array(
        [tileset_info[tileset_characters[i]] for i, c in enumerate(tileset_characters)]
    ) # must change
    values = np.vectorize(char_dict.get)(wavefunction.wf)
    
    cmap = ListedColormap(colors)
    fig, ax = plt.subplots()

    cax = ax.imshow(values, cmap, rasterized=True, vmin=0, vmax=len(tileset_info))
    cbar = fig.colorbar(cax, cmap=cmap, ticks=np.arange(0, len(tileset_info)) + 0.5)
    cbar.ax.set_yticklabels(tileset_characters)
    #dontuse ax.set_xticks(np.arange(-.5, 10, 1), minor=True)
    #dontuse ax.set_yticks(np.arange(-.5, 10, 1), minor=True)
    #ax.set_xticks(np.arange(-0.5, wavefunction.size1, 1), minor=True)
    #ax.set_yticks(np.arange(-0.5, wavefunction.size0, 1), minor=True)
    #ax.grid(which="minor", color="w", linestyle="-", linewidth=2)
    # ax.grid()
    return fig, ax

def subdivide_grid(wavefunction: Wavefunction, tileset: Tileset_wfc):
    mini_grid_size = get_mini_grid_size(tileset_info=tileset.info)
    new_size0 = wavefunction.size0*mini_grid_size
    new_size1 = wavefunction.size1*mini_grid_size
    mylist = [[ [] for i in range(new_size1)] for j in range(new_size0)]
    tileset_characters = list(tileset.info.keys())
    for j in range(wavefunction.size0):
        for i in range(wavefunction.size1):
            jj = j*mini_grid_size
            ii = i*mini_grid_size

            if len(wavefunction.wf[j][i]) == 1:
                # Just replace everything in there with the same as the cell
                for k0 in range(mini_grid_size):
                    for k1 in range(mini_grid_size):
                        mgj = jj+k0 # mini_grid_jj
                        mgi = ii+k1 # mini_grid_ii
                        mylist[mgj][mgi] = wavefunction.wf[j][i]
            else:
                # Go through each square in the mini-grid and assign the
                # corresponding character if present, or blank if not present:
                square_ind = 0 
                for k0 in range(mini_grid_size):
                    for k1 in range(mini_grid_size):
                        mgj = jj+k0 # mini_grid_jj
                        mgi = ii+k1 # mini_grid_ii
                        if square_ind >= len(tileset_characters):
                            mylist[mgj][mgi] = ["__BLANK__"]
                        elif tileset_characters[square_ind] in wavefunction.wf[j][i]:
                            mylist[mgj][mgi] = [tileset_characters[square_ind]]
                        else:
                            mylist[mgj][mgi] = ["__BLANK__"]
                        square_ind = square_ind+1
                
    return Wavefunction(mylist)


def plotting_thing(wavefunction: Wavefunction, tileset: Tileset_wfc):
    # If we dont need to split, the wavefunction is fully determined and we can
    # just plot it as normally
    determined = wavefunction.collapsed
    if determined:  # Use a normal plotting function
        fig,ax = plotting_thing_landscape(wavefunction=wavefunction, tileset=tileset)
        return fig,ax 
    subdivided = subdivide_grid(wavefunction=wavefunction, tileset=tileset)
    fig,ax = plotting_thing_landscape(wavefunction=subdivided,tileset=tileset)
    return fig, ax

    # dims:
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
