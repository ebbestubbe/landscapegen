from landscapegen.tileset import Tileset_wfc


def coast_boundary_factory():
    G = "Grass"
    W = "Water"
    S = "Sand"
    info = {
        G: [0, 1, 0, 1],
        W: [0, 0, 1, 1],
        S: [1, 1, 0, 1],
    }
    connections = {
        G: {
            "top": [G],
            "right": [G, S],
            "bottom": [G, S],
            "left": [G, S],
        },
        W: {
            "top": [W, S],
            "right": [W, S],
            "bottom": [W],
            "left": [W, S],
        },
        S: {
            "top": [G],
            "right": [W, G],
            "bottom": [W],
            "left": [W, G],
        },
    }

    tileset = Tileset_wfc(info=info, connections=connections)
    return tileset


def simple_tileset_factory():
    G = "Grass"
    W = "Water"
    S = "Sand"
    C = "Cliff"
    L = "Lava"
    info = {
        G: [0, 1, 0, 1],
        W: [0, 0, 1, 1],
        S: [1, 1, 0, 1],
        C: [0, 0, 0, 1],
        L: [1, 0, 0, 1],
    }
    connections = {
        G: {
            "top": [G, S, C],
            "right": [G, S, C],
            "bottom": [G, S, C],
            "left": [G, S, C],
        },
        W: {
            "top": [W, S],
            "right": [W, S],
            "bottom": [W, S],
            "left": [W, S],
        },
        S: {
            "top": [W, G, S],
            "right": [W, G, S],
            "bottom": [W, G, S],
            "left": [W, G, S],
        },
        L: {
            "top": [C],
            "right": [C],
            "bottom": [C],
            "left": [C],
        },
        C: {
            "top": [G, C, L],
            "right": [G, C, L],
            "bottom": [G, C, L],
            "left": [G, C, L],
        },
    }
    tileset = Tileset_wfc(info=info, connections=connections)
    return tileset
