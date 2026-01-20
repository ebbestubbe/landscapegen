import random
from pathlib import Path
from typing import Dict
from typing import List

from landscapegen.utils import flatten_list_of_lists


class Wavefunction:
    def __init__(self, wf: List[List[Dict[str, float]]]):
        # wf is a triple array where the first 2 dimensions are rectangular, and
        # the contents are arrays of strings,  eg:
        # wf = [
        #     [{"Grass": 1}, {"Grass": 0.3, "Lava": 0.7}],
        #     [{"Sand": 1}, {"Water":1}],
        #     [{"Sand":1}, {"Sand":0.1, "Grass":0.9}],
        # ]
        assert isinstance(wf[0][0], Dict)  # each cell must be a list of dicts

        self.wf = wf
        self.width = len(wf[0])
        self.height = len(wf)

    def __eq__(self, other):
        if not isinstance(other, Wavefunction):
            return False
        if (self.width != other.width) or (self.height != other.height):
            return False
        for j in range(self.width):
            for i in range(self.height):
                if not set(self.wf[j][i]) == set(other.wf[j][i]):
                    return False
                # go through each key and see if the probabilities are the same.

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

    def choose_random(cell: Dict[str, float]) -> str:
        tile = random.choices(population=list(cell.keys()), weights=list(cell.values()), k=1)[0]
        return tile

    def save(self, filename: Path):
        """Saves the wavefunction as a standard .txt.
        only saves which cell is in which position.
        Does not save color.
        Does not save probabilities.
        Assumes the wavefunction is collapsed.

        Args:
            filename (Path): filepath to save to.
        """
        assert self.collapsed

        wf_text_rows = []
        for i, row in enumerate(self.wf):
            row_text = [t[0] for t in row]  # Unpack a single row
            wf_text_rows.append(row_text)
        with open(filename, "w") as file:
            for row in wf_text_rows:
                row_text = ",".join(row) + "\n"
                file.writelines(row_text)

    def calculate_entropy(self, i: int, j: int) -> float:
        """Calculates entropy for cell (i,j)

        Args:
            i (int): _description_
            j (int): _description_

        Returns:
            float: _description_
        """
        ...


# Methods to make it easier to switch from list to dict.
def get_only_tile(cell):
    if isinstance(cell, dict):  # If its a dict, return the only key.
        assert len(cell.keys()) == 1
        key = cell.keys()[0]
        return key

    # TODO: delete
    if isinstance(cell, list):  # If its a list, assert its length==1 and return only element
        assert len(cell) == 1
        return cell[0]


def get_tile_option_list(cell):
    if isinstance(cell, dict):
        return list(cell.keys())

    # TODO: delete
    if isinstance(cell, list):
        return cell


def collapse(point, remove_in, wavefunction, tileset):
    character_set = set(tileset.characters)
    j = point[0]
    i = point[1]
    height = len(wavefunction)
    width = len(wavefunction[0])
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
        allowed_top = set(flatten_list_of_lists([tileset.connections[tile]["top"] for tile in wavefunction[j][i]]))
        forbidden_top = character_set - allowed_top
        to_remove_top = set(wavefunction[j_top][i]).intersection(forbidden_top)
        if len(to_remove_top) > 0:
            to_visit.append((coords_top, to_remove_top))
            collapse(coords_top, forbidden_top, wavefunction=wavefunction, tileset=tileset)

    # Right
    if i_right < width:  # Don't go out of scope
        coords_right = (j, i_right)
        allowed_right = set(flatten_list_of_lists([tileset.connections[tile]["right"] for tile in wavefunction[j][i]]))
        forbidden_right = character_set - allowed_right
        to_remove_right = set(wavefunction[j][i_right]).intersection(forbidden_right)
        if len(to_remove_right) > 0:
            to_visit.append((coords_right, to_remove_right))
            collapse(coords_right, to_remove_right, wavefunction=wavefunction, tileset=tileset)

    # Bottom
    if j_bottom < height:  # Don't go out of scope
        cords_bottom = (j_bottom, i)
        allowed_bottom = set(flatten_list_of_lists([tileset.connections[tile]["bottom"] for tile in wavefunction[j][i]]))
        forbidden_bottom = character_set - allowed_bottom
        to_remove_bottom = set(wavefunction[j_bottom][i]).intersection(forbidden_bottom)
        if len(to_remove_bottom) > 0:
            to_visit.append((cords_bottom, to_remove_bottom))
            collapse(cords_bottom, to_remove_bottom, wavefunction=wavefunction, tileset=tileset)

    # Left # Don't go out of scope
    if i_left >= 0:
        cords_left = (j, i_left)
        allowed_left = set(flatten_list_of_lists([tileset.connections[tile]["left"] for tile in wavefunction[j][i]]))
        forbidden_left = character_set - allowed_left
        to_remove_left = set(wavefunction[j][i_left]).intersection(forbidden_left)
        if len(to_remove_left) > 0:
            to_visit.append((cords_left, to_remove_left))
            collapse(cords_left, to_remove_left, wavefunction=wavefunction, tileset=tileset)


def generate_collapsed_wfc(tileset, height=None, width=None):
    # enerate a completely undetermined wavefunction and collapse random points until its collapsed

    wavefunction = generate_undertermined_wavefunction(tileset, height=height, width=width)

    flat_coords = get_flat_coords_of_undetermined(wavefunction=wavefunction)
    iter = 0
    while len(flat_coords) > 0:  # While we still have to figure out some coordinates.
        point = random.choice(flat_coords)  # Random point to collapse
        choice = random.choice(wavefunction[point[0]][point[1]])  #
        forbidden = set(wavefunction[point[0]][point[1]]) - set([choice])

        collapse(point, forbidden, wavefunction, tileset)

        flat_coords = get_flat_coords_of_undetermined(wavefunction=wavefunction)
        iter = iter + 1
    return Wavefunction(wavefunction)


def generate_undertermined_wavefunction(tileset, height, width):
    n_chars = len(tileset.characters)
    print(n_chars)
    # wavefunction = [[tileset.characters for _1 in range(width)] for _0 in range(height)]  # Array of all the possible tiles at this point
    wavefunction = [[{c: 1 / n_chars for c in tileset.characters} for _1 in range(width)] for _0 in range(height)]
    return wavefunction


def get_flat_coords_of_undetermined(wavefunction):
    undetermined = get_undetermined(wavefunction=wavefunction)
    coords_of_undetermined = get_coordinates_of_undetermined(wavefunction=wavefunction, undetermined=undetermined)
    flat_coords = flatten_list_of_lists(list_of_lists=coords_of_undetermined)
    return flat_coords


def get_undetermined(wavefunction):
    # bool mask for tiles if we still need to figure out what the content is.
    undetermined = [[len(subsublist) != 1 for subsublist in sublist] for sublist in wavefunction]
    return undetermined


def get_coordinates_of_undetermined(wavefunction, undetermined):
    # Coordinates we still need to figure out.
    coords = [[(j, i) for i, subsublist in enumerate(sublist) if undetermined[j][i]] for j, sublist in enumerate(wavefunction)]
    return coords
