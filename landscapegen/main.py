import copy
import random

import matplotlib.pyplot as plt
import numpy as np
from generators.random import generate_random
from matplotlib.colors import ListedColormap
from utils import flatten_list_of_lists
from utils import plot_incomplete
from utils import plot_landscape


def generate_landscape_wfc(characters, connections, size0, size1):

    character_set = set(characters)

    wavefunction = [
        [characters for _1 in range(size0)] for _2 in range(size1)
    ]  # Array of all the possible tiles at this point

    def collapse(point, remove_in):
        j = point[0]
        i = point[1]

        # Remove the stuff we hve to remove
        wavefunction[j][i] = list(set(wavefunction[j][i]) - remove_in)
        # print(f"collapsing {j},{i}")
        if len(wavefunction[j][i]) == 0:
            info = {
                "Grass": [0, 1, 0, 1],
                "Water": [0, 0, 1, 1],
                "Sand": [1, 1, 0, 1],
                "Void": [0, 0, 0, 1],
                "impossible": [1, 0, 1, 1],
            }
            wavefunc2 = copy.deepcopy(wavefunction)
            for jj in range(size1):
                for ii in range(size0):
                    if len(wavefunc2) == 0:
                        wavefunc2[jj][ii] = "Void"
                        # print(f"{jj}, {ii} is void")
                    if len(wavefunc2) > 1:
                        wavefunc2[jj][ii] = "impossible"
                        # print(f"{jj}, {ii} is impossible")
            landscape = np.array(wavefunc2)
            plot_landscape(landscape=landscape, characters=info)
            plt.show()
        assert len(wavefunction[j][i]) > 0

        # For each neighbor candidate: Dont do this if its outside the scope, and don't do it if the list of forbidden candidates is empty.
        j_top = j - 1
        i_right = i + 1
        j_bottom = j + 1
        i_left = i - 1
        to_visit = []
        # Top
        if j_top >= 0:  # Don't go out of scope
            coords_top = (j_top, i)
            allowed_top = set(
                flatten_list_of_lists(
                    [connections[tile]["top"] for tile in wavefunction[j][i]]
                )
            )
            forbidden_top = character_set - allowed_top
            to_remove_top = set(wavefunction[j_top][i]).intersection(forbidden_top)
            if len(to_remove_top) > 0:
                to_visit.append((coords_top, to_remove_top))
                collapse(coords_top, forbidden_top)

        # Right
        if i_right < size0:  # Don't go out of scope
            coords_right = (j, i_right)
            allowed_right = set(
                flatten_list_of_lists(
                    [connections[tile]["right"] for tile in wavefunction[j][i]]
                )
            )
            forbidden_right = character_set - allowed_right
            to_remove_right = set(wavefunction[j][i_right]).intersection(
                forbidden_right
            )
            if len(to_remove_right) > 0:
                to_visit.append((coords_right, to_remove_right))
                collapse(coords_right, to_remove_right)

        # Bottom
        if j_bottom < size1:  # Don't go out of scope
            cords_bottom = (j_bottom, i)
            allowed_bottom = set(
                flatten_list_of_lists(
                    [connections[tile]["bottom"] for tile in wavefunction[j][i]]
                )
            )
            forbidden_bottom = character_set - allowed_bottom
            to_remove_bottom = set(wavefunction[j_bottom][i]).intersection(
                forbidden_bottom
            )
            if len(to_remove_bottom) > 0:
                to_visit.append((cords_bottom, to_remove_bottom))
                collapse(cords_bottom, to_remove_bottom)

        # Left # Don't go out of scope
        if i_left >= 0:
            cords_left = (j, i_left)
            allowed_left = set(
                flatten_list_of_lists(
                    [connections[tile]["left"] for tile in wavefunction[j][i]]
                )
            )
            forbidden_left = character_set - allowed_left
            to_remove_left = set(wavefunction[j][i_left]).intersection(forbidden_left)
            if len(to_remove_left) > 0:
                to_visit.append((cords_left, to_remove_left))
                collapse(cords_left, to_remove_left)

    flat_coords = get_flat_coords_of_undetermined(wavefunction=wavefunction)
    iter = 0
    while len(flat_coords) > 0:  # While we still have to figure out some coordinates.
        point = random.choice(flat_coords)  # Random point to collapse
        choice = random.choice(wavefunction[point[0]][point[1]])  #
        if iter == 0:
            point = (1, 0)
            choice = "Sand"
        if iter == 1:
            point = (1, 3)
            choice = "Sand"
        forbidden = set(wavefunction[point[0]][point[1]]) - set([choice])

        print(point, wavefunction[point[0]][point[1]], choice)
        collapse(point, forbidden)
        plot_incomplete(wavefunction=wavefunction)
        flat_coords = get_flat_coords_of_undetermined(wavefunction=wavefunction)
        iter = iter + 1
    return np.array(wavefunction)


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


# def plot_landscape(landscape, characters):

#     char_list = list(
#         characters.keys()
#     )  # Position in this is value, We do this once so the value is locked for each tile
#     char_dict = {c: i for i, c in enumerate(char_list)}  # tile: value
#     values = np.vectorize(char_dict.get)(landscape)
#     colors = np.array([characters[char_list[i]] for i, c in enumerate(char_list)])
#     cmap = ListedColormap(colors)
#     fig, ax = plt.subplots()

#     cax = ax.imshow(values, cmap, rasterized=True, vmin=0, vmax=len(characters))
#     cbar = fig.colorbar(cax, cmap=cmap, ticks=np.arange(0, len(characters)) + 0.5)
#     cbar.ax.set_yticklabels(char_list)
#     plt.show()


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
    plot_landscape(landscape=landscape, characters=info)


def run3():
    size0 = 5
    size1 = 5
    info = {
        "Grass": [0, 1, 0, 1],
        "Water": [0, 0, 1, 1],
        "Sand": [1, 1, 0, 1],
        "Cliff": [0, 0, 0, 1],
        "Lava": [1, 0, 0, 1],
    }
    connections4 = {
        "Grass": {
            "top": ["Grass", "Sand", "Cliff"],
            "right": ["Grass", "Sand", "Cliff"],
            "bottom": ["Grass", "Sand", "Cliff"],
            "left": ["Grass", "Sand", "Cliff"],
        },
        "Water": {
            "top": ["Water", "Sand"],
            "right": ["Water", "Sand"],
            "bottom": ["Water", "Sand"],
            "left": ["Water", "Sand"],
        },
        "Sand": {
            "top": ["Water", "Grass", "Sand"],
            "right": ["Water", "Grass", "Sand"],
            "bottom": ["Water", "Grass", "Sand"],
            "left": ["Water", "Grass", "Sand"],
        },
        "Lava": {
            "top": ["Cliff"],
            "right": ["Cliff"],
            "bottom": ["Cliff"],
            "left": ["Cliff"],
        },
        "Cliff": {
            "top": ["Grass", "Cliff", "Lava"],
            "right": ["Grass", "Cliff", "Lava"],
            "bottom": ["Grass", "Cliff", "Lava"],
            "left": ["Grass", "Cliff", "Lava"],
        },
    }
    characters = list(info.keys())
    landscape = generate_landscape_wfc(
        characters=characters, connections=connections4, size0=size0, size1=size1
    )
    plot_landscape(landscape=landscape, characters=info)


def run4():
    size0 = 50
    size1 = 50
    info = {
        "Grass": [0, 1, 0, 1],
        "Water": [0, 0, 1, 1],
        "Sand": [1, 1, 0, 1],
        # "Cliff": [0, 0, 0, 1],
        # "Lava": [1, 0, 0, 1],
    }
    G = "Grass"
    W = "Water"
    S = "Sand"
    connections = {
        "Grass": {
            "top": [G],
            "right": [G, S],
            "bottom": [G, S],
            "left": [G, S],
        },
        "Water": {
            "top": [W, S],
            "right": [W, S],
            "bottom": [W],
            "left": [W, S],
        },
        "Sand": {
            "top": [G],
            "right": [W, G],
            "bottom": [W],
            "left": [W, G],
        },
    }
    characters = list(info.keys())
    landscape = generate_landscape_wfc(
        characters=characters, connections=connections, size0=size0, size1=size1
    )
    plot_landscape(landscape=landscape, characters=info)


def run5():
    size0 = 4
    size1 = 3
    info = {
        "Grass": [0, 1, 0, 1],
        "Water": [0, 0, 1, 1],
        "Sand": [1, 1, 0, 1],
        # "Cliff": [0, 0, 0, 1],
        # "Lava": [1, 0, 0, 1],
    }
    G = "Grass"
    W = "Water"
    S = "Sand"
    connections = {
        "Grass": {
            "top": [G],
            "right": [G, S],
            "bottom": [G, S],
            "left": [G, S],
        },
        "Water": {
            "top": [W, S],
            "right": [W, S],
            "bottom": [W],
            "left": [W, S],
        },
        "Sand": {
            "top": [G],
            "right": [W, G],
            "bottom": [W],
            "left": [W, G],
        },
    }
    characters = list(info.keys())
    landscape = generate_landscape_wfc(
        characters=characters, connections=connections, size0=size0, size1=size1
    )
    plot_landscape(landscape=landscape, characters=info)


def main():
    run5()

    plt.show()


if __name__ == "__main__":
    main()