from landscapegen.utils import get_mini_grid_size


def test_landscape_1():
    info = {
        "Grass": [0, 1, 0, 1],
    }
    mini_grid_size = get_mini_grid_size(info)
    expected = 1
    assert mini_grid_size == expected


def test_landscape_2():

    info = {
        "Grass": [0, 1, 0, 1],
        "Water": [0, 0, 1, 1],
    }
    mini_grid_size = get_mini_grid_size(info)
    expected = 4
    assert mini_grid_size == expected


def test_landscape_3():
    info = {
        "Grass": [0, 1, 0, 1],
        "Water": [0, 0, 1, 1],
        "Sand": [1, 1, 0, 1],
        "Cliff": [0, 0, 0, 1],
    }
    mini_grid_size = get_mini_grid_size(info)
    expected = 4
    assert mini_grid_size == expected


def test_landscape_4():
    info = {
        "Grass": [0, 1, 0, 1],
        "Water": [0, 0, 1, 1],
        "Sand": [1, 1, 0, 1],
        "Cliff": [0, 0, 0, 1],
        "Lava": [1, 0, 0, 1],
    }
    mini_grid_size = get_mini_grid_size(info)
    expected = 9
    assert mini_grid_size == expected
