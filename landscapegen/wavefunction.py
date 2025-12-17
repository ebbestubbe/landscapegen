import random
from typing import List

from landscapegen.utils import flatten_list_of_lists


class Wavefunction:
    def __init__(self, wf: List[List[List[str]]]):
        # wf is a triple array where the first 2 dimensions are rectangular, and
        # the contents are arrays of strings,  eg:
        # wf = [
        #     [["Grass"], ["Grass", "Lava"]],
        #     [["Sand"], ["Water"]],
        #     [["Sand"], ["Sand", "Grass"]],
        # ]
        self.wf = wf
        self.size0 = len(wf[0])
        self.size1 = len(wf)
        self.width = self.size0
        self.height = self.size1

    def __eq__(self, other):
        if not isinstance(other, Wavefunction):
            return False
        if (self.size0 != other.size0) or (self.size1 != other.size1):
            return False
        for j in range(self.size0):
            for i in range(self.size1):
                if not set(self.wf[j][i]) == set(other.wf[j][i]):
                    return False
        return True

    @property
    def collapsed(self):
        # Go through all points and figure out of there are more than 1 element
        # in each.
        for i, row in enumerate(self.wf):
            for j, col in enumerate(row):
                if len(col) > 1:
                    return False
        return True

    @property
    def contains_blank(self):
        for i, row in enumerate(self.wf):
            for j, col in enumerate(row):
                if col[0] == "__BLANK__":
                    return True

        return False


def collapse(point, remove_in, wavefunction, tileset, width, height):
    character_set = set(tileset.characters)
    j = point[0]
    i = point[1]

    # Remove the stuff we have to remove
    wavefunction[j][i] = list(set(wavefunction[j][i]) - remove_in)
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
                [tileset.connections[tile]["top"] for tile in wavefunction[j][i]]
            )
        )
        forbidden_top = character_set - allowed_top
        to_remove_top = set(wavefunction[j_top][i]).intersection(forbidden_top)
        if len(to_remove_top) > 0:
            to_visit.append((coords_top, to_remove_top))
            collapse(
                coords_top,
                forbidden_top,
                wavefunction=wavefunction,
                tileset=tileset,
                width=width,
                height=height,
            )

    # Right
    if i_right < width:  # Don't go out of scope
        coords_right = (j, i_right)
        allowed_right = set(
            flatten_list_of_lists(
                [tileset.connections[tile]["right"] for tile in wavefunction[j][i]]
            )
        )
        forbidden_right = character_set - allowed_right
        to_remove_right = set(wavefunction[j][i_right]).intersection(forbidden_right)
        if len(to_remove_right) > 0:
            to_visit.append((coords_right, to_remove_right))
            collapse(
                coords_right,
                to_remove_right,
                wavefunction=wavefunction,
                tileset=tileset,
                width=width,
                height=height,
            )

    # Bottom
    if j_bottom < height:  # Don't go out of scope
        cords_bottom = (j_bottom, i)
        allowed_bottom = set(
            flatten_list_of_lists(
                [tileset.connections[tile]["bottom"] for tile in wavefunction[j][i]]
            )
        )
        forbidden_bottom = character_set - allowed_bottom
        to_remove_bottom = set(wavefunction[j_bottom][i]).intersection(forbidden_bottom)
        if len(to_remove_bottom) > 0:
            to_visit.append((cords_bottom, to_remove_bottom))
            collapse(
                cords_bottom,
                to_remove_bottom,
                wavefunction=wavefunction,
                tileset=tileset,
                width=width,
                height=height,
            )

    # Left # Don't go out of scope
    if i_left >= 0:
        cords_left = (j, i_left)
        allowed_left = set(
            flatten_list_of_lists(
                [tileset.connections[tile]["left"] for tile in wavefunction[j][i]]
            )
        )
        forbidden_left = character_set - allowed_left
        to_remove_left = set(wavefunction[j][i_left]).intersection(forbidden_left)
        if len(to_remove_left) > 0:
            to_visit.append((cords_left, to_remove_left))
            collapse(
                cords_left,
                to_remove_left,
                wavefunction=wavefunction,
                tileset=tileset,
                width=width,
                height=height,
            )


def generate_collapsed_wfc(tileset, height=None, width=None):
    # enerate a completely undetermined wavefunction and collapse random points until its collapsed

    wavefunction = generate_undertermined_wavefunction(
        tileset, height=height, width=width
    )

    flat_coords = get_flat_coords_of_undetermined(wavefunction=wavefunction)
    iter = 0
    while len(flat_coords) > 0:  # While we still have to figure out some coordinates.
        point = random.choice(flat_coords)  # Random point to collapse
        choice = random.choice(wavefunction[point[0]][point[1]])  #
        forbidden = set(wavefunction[point[0]][point[1]]) - set([choice])

        collapse(point, forbidden, wavefunction, tileset, width, height)

        flat_coords = get_flat_coords_of_undetermined(wavefunction=wavefunction)
        iter = iter + 1
    return Wavefunction(wavefunction)


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
