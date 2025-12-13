import copy
import random

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

from landscapegen.factory import coast_boundary_factory
from landscapegen.factory import simple_tileset_factory
from landscapegen.generators.random import generate_random
from landscapegen.matplotlib_plotting import plot_incomplete
from landscapegen.matplotlib_plotting import plot_landscape
from landscapegen.matplotlib_plotting import plotting_thing
from landscapegen.matplotlib_plotting import subdivide_grid
from landscapegen.pygqt_plotting import pyqt_plot
from landscapegen.utils import flatten_list_of_lists
from landscapegen.wavefunction import collapse
from landscapegen.wavefunction import Wavefunction


def generate_landscape_wfc(tileset, size0=None, size1=None, height=None, width=None):
    assert (size1 is None and height is not None) or (
        size1 is not None and height is None
    )  # legacy fix, use height instead of size1
    assert (size0 is None and width is not None) or (
        size0 is not None and width is None
    )  # legacy fix, use width instead of size0

    height = height or size1
    width = width or size0

    wavefunction = generate_undertermined_wavefunction(
        tileset, height=height, width=width
    )

    flat_coords = get_flat_coords_of_undetermined(wavefunction=wavefunction)
    iter = 0
    while len(flat_coords) > 0:  # While we still have to figure out some coordinates.
        point = random.choice(flat_coords)  # Random point to collapse
        choice = random.choice(wavefunction[point[0]][point[1]])  #
        # # Debug coast boundary
        # if iter == 0:
        #     point = (1, 0)
        #     choice = "Sand"
        # if iter == 1:
        #     point = (1, 3)
        #     choice = "Sand"
        forbidden = set(wavefunction[point[0]][point[1]]) - set([choice])

        # print(point, wavefunction[point[0]][point[1]], choice)
        collapse(point, forbidden, wavefunction, tileset, width, height)
        # plot_incomplete(wavefunction=wavefunction)
        flat_coords = get_flat_coords_of_undetermined(wavefunction=wavefunction)
        iter = iter + 1
    return Wavefunction(wavefunction)
    return np.array(wavefunction)


def generate_undertermined_wavefunction(tileset, height, width):

    wavefunction = [
        [tileset.characters for _1 in range(width)] for _0 in range(height)
    ]  # Array of all the possible tiles at this point
    return wavefunction


def get_flat_coords_of_undetermined(wavefunction):
    undetermined = get_undetermined(wavefunction=wavefunction)
    coords_of_undetermined = get_coordinates_of_undetermined(
        wavefunction=wavefunction, undetermined=undetermined
    )
    flat_coords = flatten_list_of_lists(list_of_lists=coords_of_undetermined)
    return flat_coords


def get_undetermined(wavefunction):
    # bool mask for tiles if we still need to figure out what the content is.
    undetermined = [
        [len(subsublist) != 1 for subsublist in sublist] for sublist in wavefunction
    ]
    return undetermined


def get_coordinates_of_undetermined(wavefunction, undetermined):
    # Coordinates we still need to figure out.
    coords = [
        [(j, i) for i, subsublist in enumerate(sublist) if undetermined[j][i]]
        for j, sublist in enumerate(wavefunction)
    ]
    return coords


def run1():
    size0 = 2
    size1 = 4
    characters = {
        "Grass": [0, 1, 0, 1],
        "Water": [0, 0, 1, 1],
        "Sand": [1, 1, 0, 1],
    }

    landscape = generate_random(
        characters=list(characters.keys()), size0=size0, size1=size1
    )
    print(landscape)
    plot_landscape(landscape, characters)


def run2():
    size0 = 10
    size1 = 10
    info = {
        "Grass": [0, 1, 0, 1],
        "Water": [0, 0, 1, 1],
        "Sand": [1, 1, 0, 1],
        "Cliff": [0, 0, 0, 1],
        "Lava": [1, 0, 0, 1],
    }
    characters = list(info.keys())
    landscape = generate_random(characters=characters, size0=size0, size1=size1)
    plot_landscape(landscape=landscape, tileset_info=info)


def run3():
    size0 = 5
    size1 = 10

    tileset = simple_tileset_factory()

    landscape = generate_landscape_wfc(tileset=tileset, size0=size0, size1=size1)
    plot_landscape(landscape=landscape, tileset_info=tileset.info)


def run_buggy_coast():
    size0 = 4
    size1 = 3

    tileset = coast_boundary_factory()

    landscape = generate_landscape_wfc(tileset=tileset, size0=size0, size1=size1)
    plot_landscape(landscape=landscape, tileset_info=tileset.info)


def run_buggy_coast2():
    size0 = 4
    size1 = 3

    tileset = coast_boundary_factory()

    landscape = generate_landscape_wfc(tileset=tileset, size0=size0, size1=size1)
    plotting_thing(wavefunction=Wavefunction(landscape), tileset=tileset)


def plot_example_determined():
    # size0 = 4
    # size1 = 3

    tileset = simple_tileset_factory()
    tileset = coast_boundary_factory()
    # wavefunction = [
    #     [tileset.characters for _1 in range(size0)] for _2 in range(size1)
    # ]  # Array of all the possible tiles at this point
    landscape = [
        [["Grass"], ["Grass"], ["Grass"], ["Grass"], ["Grass"]],
        [["Sand"], ["Water"], ["Grass"], ["Grass"], ["Grass"]],
        [["Sand"], ["Sand"], ["Grass"], ["Grass"], ["Grass"]],
        [["Grass"], ["Grass"], ["Grass"], ["Grass"], ["Grass"]],
        [["Sand"], ["Water"], ["Grass"], ["Grass"], ["Grass"]],
    ]
    wavefunction = Wavefunction(landscape)
    # plotting_thing(wavefunction=wavefunction, tileset=tileset)
    split, grid_size = subdivide_grid(wavefunction=wavefunction, tileset=tileset)
    # plot_incomplete(wavefunction=split.wf, tileset=tileset)
    plotting_thing(wavefunction=split, tileset=tileset)
    plt.show()


def plot_example_undetermined():
    # size0 = 4
    # size1 = 3

    # tileset = simple_tileset_factory()
    tileset = coast_boundary_factory()
    # wavefunction = [
    #     [tileset.characters for _1 in range(size0)] for _2 in range(size1)
    # ]  # Array of all the possible tiles at this point
    landscape = [
        [["Grass"], ["Grass"], ["Grass"], ["Grass"], ["Grass"]],
        [["Sand"], ["Water"], ["Grass"], ["Grass"], ["Grass"]],
        [["Sand"], ["Sand"], ["Grass", "Water"], ["Grass"], ["Grass"]],
        [["Grass"], ["Grass"], ["Grass"], ["Grass"], ["Grass", "Sand"]],
        [["Sand"], ["Water"], ["Grass"], ["Grass"], ["Grass"]],
    ]
    wavefunction = Wavefunction(landscape)
    fig, ax = plotting_thing(wavefunction=wavefunction, tileset=tileset)
    # Almost, just need to take care of the 'blanks
    # plot_incomplete(wavefunction=landscape, tileset=tileset)
    plt.show()


def plot_example_undetermined_small():
    # size0 = 4
    # size1 = 3

    # tileset = simple_tileset_factory()
    tileset = coast_boundary_factory()
    # wavefunction = [
    #     [tileset.characters for _1 in range(size0)] for _2 in range(size1)
    # ]  # Array of all the possible tiles at this point
    landscape = [
        [["Grass", "Sand"], ["Grass"]],
        [["Sand"], ["Water"]],
    ]
    wavefunction = Wavefunction(landscape)
    fig, ax = plotting_thing(wavefunction=wavefunction, tileset=tileset)
    # Almost, just need to take care of the 'blanks
    # plot_incomplete(wavefunction=landscape, tileset=tileset)
    plt.show()


def plot_example_determined_small():
    # size0 = 4
    # size1 = 3

    # tileset = simple_tileset_factory()
    tileset = coast_boundary_factory()
    # wavefunction = [
    #     [tileset.characters for _1 in range(size0)] for _2 in range(size1)
    # ]  # Array of all the possible tiles at this point
    landscape = [
        [["Water"], ["Grass"]],
        [["Sand"], ["Water", "Grass"]],
    ]
    wavefunction = Wavefunction(landscape)
    fig, ax = plotting_thing(wavefunction=wavefunction, tileset=tileset)
    # Almost, just need to take care of the 'blanks
    # plot_incomplete(wavefunction=landscape, tileset=tileset)
    plt.show()


def plot_example_pyqt():

    tileset = coast_boundary_factory()
    landscape = [
        [["Grass"], ["Grass"], ["Grass"], ["Grass"], ["Grass"]],
        [["Sand"], ["Water"], ["Grass"], ["Grass"], ["Grass"]],
        [["Sand"], ["Sand"], ["Grass"], ["Grass"], ["Grass"]],
        [["Grass"], ["Grass"], ["Grass"], ["Grass"], ["Grass"]],
        [["Sand"], ["Water"], ["Grass"], ["Grass"], ["Grass"]],
    ]
    wavefunction = Wavefunction(landscape)
    # plotting_thing(wavefunction=wavefunction, tileset=tileset)
    split, grid_size = subdivide_grid(wavefunction=wavefunction, tileset=tileset)
    # plot_incomplete(wavefunction=split.wf, tileset=tileset)
    plotting_thing(wavefunction=split, tileset=tileset)
    from landscapegen.pygqt_plotting import pyqt_plot

    pyqt_plot(wavefunction=wavefunction, tileset=tileset)


def plot_example_pyqt_2():
    height = 10
    width = 15

    tileset = simple_tileset_factory()

    wavefunction = generate_landscape_wfc(tileset=tileset, height=height, width=width)
    from landscapegen.pygqt_plotting import pyqt_plot

    pyqt_plot(wavefunction=wavefunction, tileset=tileset)


def plot_example_pyqt_undertermined():

    tileset = coast_boundary_factory()
    landscape = [
        [["Grass"], ["Grass"], ["Grass"], ["Grass"], ["Grass"]],
        [["Sand"], ["Water"], ["Grass"], ["Grass"], ["Grass"]],
        [["Sand"], ["Sand"], ["Grass", "Water"], ["Grass"], ["Grass"]],
        [["Grass"], ["Grass"], ["Grass"], ["Grass"], ["Grass", "Sand"]],
        [["Sand"], ["Water"], ["Grass"], ["Grass"], ["Grass"]],
    ]
    wavefunction = Wavefunction(landscape)

    pyqt_plot(wavefunction=wavefunction, tileset=tileset)


def plot_completely_undetermined_coast():
    height = 7
    width = 10
    tileset = coast_boundary_factory()
    wavefunction = generate_undertermined_wavefunction(
        tileset=tileset, height=height, width=width
    )
    wavefunction = Wavefunction(wavefunction)
    pyqt_plot(wavefunction=wavefunction, tileset=tileset)


def plot_completely_undetermined_simple():
    height = 7
    width = 10
    tileset = simple_tileset_factory()
    wavefunction = generate_undertermined_wavefunction(
        tileset=tileset, height=height, width=width
    )
    wavefunction = Wavefunction(wavefunction)
    pyqt_plot(wavefunction=wavefunction, tileset=tileset)


def main():
    # plot_example_determined()
    # plot_example_undetermined()
    # plot_example_determined_small()
    # plot_example_undetermined_small()

    # plot_example_determined_small()

    # run3()
    # plt.show()

    # plot_example_pyqt()
    # plot_example_pyqt_2()
    # plot_example_pyqt_undertermined()
    # plot_completely_undetermined_coast()
    plot_completely_undetermined_simple()


if __name__ == "__main__":

    main()
