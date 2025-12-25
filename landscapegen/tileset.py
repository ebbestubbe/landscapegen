from pathlib import Path

from landscapegen.utils import flatten_list_of_lists
from landscapegen.wavefunction import Wavefunction


class Tileset_wfc:
    # Only to be used with wave function collapse
    def __init__(self, info, connections) -> None:
        self.info = info
        self.connections = connections
        self.characters = list(self.info.keys())


default_info = {
    "Grass": [0, 1, 0, 1],
    "Water": [0, 0, 1, 1],
    "Sand": [1, 1, 0, 1],
    "Cliff": [0, 0, 0, 1],
    "Lava": [1, 0, 0, 1],
}


def get_neighbor_inds(i, j, height, width):
    neighbors = []
    if i > 0:  # add top
        neighbors.append((i - 1, j))
    if i < height - 1:  # add bottom
        neighbors.append((i + 1, j))
    if j > 0:  # add left
        neighbors.append((i, j - 1))
    if j < width - 1:  # add right
        neighbors.append((i, j + 1))
    return neighbors


def get_bidirectional_neighbor_set(path):
    # Assumptions:
    # Non directionality: that all directions are the same. no difference if a tile is up, down, left or right
    # Symmetry: This means that neighbor pairs (a,b) is also (b,a)

    # method: For each tile, find all neighbors and add both combinations.

    # Count all pairs
    with open(path) as f:
        lines = f.readlines()
    list_of_lists = [line.strip("\n").split(",") for line in lines]
    height = len(list_of_lists)
    width = len(list_of_lists[0])

    neighbor_set = set()
    for i in range(height):
        for j in range(width):
            neighbors = get_neighbor_inds(i, j, height, width)
            tile_ij = list_of_lists[i][j]
            for n in neighbors:
                tile_neighbor = list_of_lists[n[0]][n[1]]
                neighbor_set.add((tile_ij, tile_neighbor))
                neighbor_set.add((tile_neighbor, tile_ij))
    return neighbor_set


def tileset_from_save(path: Path):
    with open(path) as f:
        lines = f.readlines()

    # Make a collapsed wf:
    wf = [[[tile] for tile in line.strip("\n").split(",")] for line in lines]
    wavefunction = Wavefunction(wf)
    print("=" * 50 + "wf" + "=" * 50)
    print(wavefunction.wf)
    print("=" * 50 + "wf[0]" + "=" * 50)
    print(wavefunction.wf[0])
    list_of_lists = [line.strip("\n").split(",") for line in lines]
    print("=" * 50 + "list of lists" + "=" * 50)
    print(list_of_lists)
    flat = flatten_list_of_lists(list_of_lists)

    print("=" * 50 + "flat" + "=" * 50)
    print(flat)
    height = len(list_of_lists)
    width = len(list_of_lists[0])
    print("=" * 50 + "number of tiles" + "=" * 50)
    n_tiles = len(flat)
    print("[height x width]", f"[{height} x {width}]", "=", n_tiles)
    chars = set(flat)
    print("=" * 50 + "chars" + "=" * 50)
    print(chars)

    counts = {}
    for element in flat:
        counts[element] = counts.get(element, 0) + 1

    print("=" * 50 + "counts" + "=" * 50)
    print(counts)
    print("=" * 50 + "frequencies" + "=" * 50)
    print({k: v / n_tiles for k, v in counts.items()})

    # Assumptions:
    # Non directionality: that all directions are the same. no difference if a tile is up, down, left or right
    # Symmetry: This means that neighbor pairs (a,b) is also (b,a)

    # method: For each tile, find all neighbors and add both combinations.

    # Count all pairs
    neighbors = get_bidirectional_neighbor_set(path)
    print(neighbors)
    connections = {}
    for char in chars:
        neighbor_tiles_allowed = [n[1] for n in neighbors if n[0] == char]
        connections[char] = {
            "top": neighbor_tiles_allowed,
            "bottom": neighbor_tiles_allowed,
            "left": neighbor_tiles_allowed,
            "right": neighbor_tiles_allowed,
        }
    from pprint import pprint

    pprint(connections)
    info = {k: v for k, v in default_info.items() if k in connections}
    return Tileset_wfc(info=info, connections=connections)
