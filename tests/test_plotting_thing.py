from landscapegen.utils import get_mini_grid_size
from landscapegen.utils import subdivide_grid
from landscapegen.tileset import Tileset_wfc
from landscapegen.wavefunction import Wavefunction
def test_get_mini_grid_size_fit_1():
    info = {
        "Grass": [0, 1, 0, 1],
    }
    mini_grid_size = get_mini_grid_size(info)
    expected = 1
    assert mini_grid_size == expected


def test_get_mini_grid_size_2():

    info = {
        "Grass": [0, 1, 0, 1],
        "Water": [0, 0, 1, 1],
    }
    mini_grid_size = get_mini_grid_size(info)
    expected = 2
    assert mini_grid_size == expected


def test_get_mini_grid_size_fit_4():
    info = {
        "Grass": [0, 1, 0, 1],
        "Water": [0, 0, 1, 1],
        "Sand": [1, 1, 0, 1],
        "Cliff": [0, 0, 0, 1],
    }
    mini_grid_size = get_mini_grid_size(info)
    expected = 2
    assert mini_grid_size == expected


def test_get_mini_grid_size_5():
    info = {
        "Grass": [0, 1, 0, 1],
        "Water": [0, 0, 1, 1],
        "Sand": [1, 1, 0, 1],
        "Cliff": [0, 0, 0, 1],
        "Lava": [1, 0, 0, 1],
    }
    mini_grid_size = get_mini_grid_size(info)
    expected = 3
    assert mini_grid_size == expected


def test_subdivide_grid_simple():
    info = {
        "Grass": [0, 1, 0, 1],
        "Water": [0, 0, 1, 1],
        "Sand": [1, 1, 0, 1]
    }
    wavefunction = Wavefunction(
        [
            [["Grass"], ["Sand"],],
            [["Sand"], ["Water"],],
        ]
    )
    tileset = Tileset_wfc(info = info, connections=None)
    expected = Wavefunction(
        [
            [["Grass"], ["Grass"],      ["Sand"], ["Sand"]],
            [["Grass"], ["Grass"],       ["Sand"], ["Sand"]],
            [["Sand"],  ["Sand"],        ["Water"], ["Water"]],
            [["Sand"],  ["Sand"],        ["Water"], ["Water"]],
        ]
    )
    subdivided = subdivide_grid(wavefunction, tileset)
    assert subdivided == expected


def test_subdivide_grid_2x2():
    info = {
        "Grass": [0, 1, 0, 1],
        "Water": [0, 0, 1, 1],
        "Sand": [1, 1, 0, 1]
    }
    wavefunction = Wavefunction(
        [
            [["Grass"], ["Grass", "Sand"],],
            [["Sand"], ["Water"],],
        ]
    )
    tileset = Tileset_wfc(info = info, connections=None)
    expected = Wavefunction(
        [
            [["Grass"], ["Grass"],      ["Grass"], ["__BLANK__"]],
            [["Grass"], ["Grass"],       ["Sand"],   ["__BLANK__"]],
            [["Sand"],  ["Sand"],        ["Water"], ["Water"]],
            [["Sand"],  ["Sand"],        ["Water"], ["Water"]],
        ]
    )
    subdivided = subdivide_grid(wavefunction, tileset)
    assert subdivided == expected