import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
import random


def generate_landscape_random(characters, size0, size1):

    possibilities = [[characters for _1 in range(size0)] for _2 in range(size1)]
    choice = [[random.choice(subsublist) for subsublist in sublist] for sublist in possibilities]
    landscape = np.array(choice)
    #landscape = np.random.choice(characters, size0*size1).reshape(size0,size1)
    return landscape

def flatten_list_of_lists(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]

def generate_landscape_wfc(characters, connections, size0, size1):
    
    character_set = set(characters)
    #rules:
    

    wavefunction = [[characters for _1 in range(size0)] for _2 in range(size1)]
    def collapse(point, remove_in):
        j = point[0] 
        i = point[1]

        #Remove the stuff we hve to remove
        wavefunction[j][i] = list(set(wavefunction[j][i]) - remove_in)
        assert len(wavefunction[j][i]) > 0
        
        #For each neighbor candidate: Dont do this if its outside the scope, and don't do it if the list of forbidden candidates is empty.
        j_top = j-1
        i_right = i+1
        j_bottom = j+1
        i_left = i-1
        to_visit = []
        #Top
        if j_top >= 0:
            coords_top = (j_top, i)
            allowed_top = set(flatten_list_of_lists([connections[tile]['top'] for tile in wavefunction[j][i]]))
            forbidden_top = character_set - allowed_top
            to_remove_top = set(wavefunction[j_top][i]).intersection(forbidden_top)
            if len(to_remove_top) > 0:
                to_visit.append((coords_top, to_remove_top))
                collapse(coords_top, forbidden_top)

        #Right
        if i_right < size0:
            coords_right = (j, i_right)
            allowed_right = set(flatten_list_of_lists([connections[tile]['right'] for tile in wavefunction[j][i]]))
            forbidden_right = character_set - allowed_right
            to_remove_right = set(wavefunction[j][i_right]).intersection(forbidden_right)
            if len(to_remove_right) > 0:
                to_visit.append((coords_right, to_remove_right))
                collapse(coords_right, to_remove_right)

        #Bottom
        if j_bottom < size1:
            cords_bottom = (j_bottom, i)
            allowed_bottom = set(flatten_list_of_lists([connections[tile]['bottom'] for tile in wavefunction[j][i]]))
            forbidden_bottom = character_set - allowed_bottom
            to_remove_bottom = set(wavefunction[j_bottom][i]).intersection(forbidden_bottom)
            if len(to_remove_bottom) > 0:
                to_visit.append((cords_bottom, to_remove_bottom))
                collapse(cords_bottom, to_remove_bottom)

        #Left
        if i_left >= 0:
            cords_left = (j, i_left)
            allowed_left = set(flatten_list_of_lists([connections[tile]['left'] for tile in wavefunction[j][i]]))
            forbidden_left = character_set - allowed_left
            to_remove_left = set(wavefunction[j][i_left]).intersection(forbidden_left)
            if len(to_remove_left) > 0:
                to_visit.append((cords_left, to_remove_left))
                collapse(cords_left, to_remove_left)
    #wavefunction_np = np.array([['; '.join(tilelist) for tilelist in sublist] for sublist in wavefunction])
    undetermined = [[len(subsublist)!=1 for subsublist in sublist] for sublist in wavefunction]
    coords = [[(j,i) for i,subsublist in enumerate(sublist) if undetermined[j][i]] for j,sublist in enumerate(wavefunction)]
    flat_coords = [item for sublist in coords for item in sublist]
    while len(flat_coords) > 0:
        point = random.choice(flat_coords)
        #forbidden = set(["Water"]) #hardcode - random choice from list at random point
        choice = random.choice(wavefunction[point[0]][point[1]])
        forbidden = set(wavefunction[point[0]][point[1]]) - set([choice])


        collapse(point, forbidden)
        undetermined = [[len(subsublist)!=1 for subsublist in sublist] for sublist in wavefunction]
        coords = [[(j,i) for i,subsublist in enumerate(sublist) if undetermined[j][i]] for j,sublist in enumerate(wavefunction)]
        flat_coords = [item for sublist in coords for item in sublist]


    return np.array(wavefunction)


def plot_landscape(landscape, characters):

    char_list = list(characters.keys()) #Position in this is value, We do this once so the value is locked for each tile 
    char_dict = {c: i for i,c in enumerate(char_list)} # tile: value
    values = np.vectorize(char_dict.get)(landscape)
    colors = np.array([characters[char_list[i]] for i,c in enumerate(char_list)])
    cmap = ListedColormap(colors)
    fig,ax = plt.subplots()

    cax = ax.imshow(values, cmap, rasterized=True,vmin=0, vmax=len(characters))
    cbar = fig.colorbar(cax, cmap=cmap, ticks=np.arange(0,len(characters))+0.5)
    cbar.ax.set_yticklabels(char_list)
    plt.show()


def run1():
    size0 = 2
    size1 = 4
    characters = {
        'Grass': [0,1,0,1],
        'Water': [0,0,1,1],
        'Sand': [1,1,0,1],
    }
    

    landscape = generate_landscape_random(characters=list(characters.keys()), size0=size0,size1 = size1)
    print(landscape)
    plot_landscape(landscape,characters)

def depth_first_grid():
    coords = [[(j,i) for i in range(5)] for j in range(5)]

    j = 3
    i = 1
    coords[j][i]
    to_visit = []
    neighbor_0 = coords[j-1][i]
    neighbor_1 = coords[j][i+1]
    neighbor_2 = coords[j+1][i]
    neighbor_3 = coords[j][i-1]
    to_visit.append(neighbor_0)
    to_visit.append(neighbor_1)
    to_visit.append(neighbor_2)
    to_visit.append(neighbor_3)

    print("f99")

def main():
    #run1()

    size0 = 50
    size1 = 50
    info = {
        'Grass': [0,1,0,1],
        'Water': [0,0,1,1],
        'Sand': [1,1,0,1],
        "Cliff": [0,0,0,1],
        "Lava": [1,0,0,1]
    }
    characters=list(info.keys())
    connections1 = {
        "Grass": {
            "top": ["Grass"],
            "right": ["Grass"],
            "bottom": ["Grass"],
            "left": ["Grass"]
        },
        "Water": {
            "top": ["Water"],
            "right": ["Water"],
            "bottom": ["Water"],
            "left": ["Water"]
        }
    }
    connections2 = {
        "Grass": {
            "top": ["Grass", "Water"],
            "right": ["Water"],
            "bottom": ["Grass", "Water"],
            "left": ["Water"]
        },
        "Water": {
            "top": ["Grass", "Water"],
            "right": ["Grass"],
            "bottom": ["Grass", "Water"],
            "left": ["Grass"]
        }
    }
    connections3 = {
        "Grass": {
            "top": ["Grass", "Sand"],
            "right": ["Grass", "Sand"],
            "bottom": ["Grass", "Sand"],
            "left": ["Grass", "Sand"]
        },
        "Water": {
            "top": ["Water", "Sand"],
            "right": ["Water", "Sand"],
            "bottom": ["Water", "Sand"],
            "left": ["Water", "Sand"]
        },
        "Sand": {
            "top": ["Water", "Grass", "Sand"],
            "right": ["Water", "Grass", "Sand"],
            "bottom": ["Water", "Grass", "Sand"],
            "left": ["Water", "Grass", "Sand"]
        }
    }
    connections4 = {
        "Grass": {
            "top": ["Grass", "Sand", "Cliff"],
            "right": ["Grass", "Sand", "Cliff"],
            "bottom": ["Grass", "Sand", "Cliff"],
            "left": ["Grass", "Sand", "Cliff"]
        },
        "Water": {
            "top": ["Water", "Sand"],
            "right": ["Water", "Sand"],
            "bottom": ["Water", "Sand"],
            "left": ["Water", "Sand"]
        },
        "Sand": {
            "top": ["Water", "Grass", "Sand"],
            "right": ["Water", "Grass", "Sand"],
            "bottom": ["Water", "Grass", "Sand"],
            "left": ["Water", "Grass", "Sand"]
        },
        "Lava": {
            "top": ["Cliff"],
            "right": ["Cliff"],
            "bottom": ["Cliff"],
            "left": ["Cliff"]
        },
        "Cliff": {
            "top": ["Grass", "Cliff", "Lava"],
            "right": ["Grass", "Cliff", "Lava"],
            "bottom": ["Grass", "Cliff", "Lava"],
            "left": ["Grass", "Cliff", "Lava"]
        }
    }
    landscape = generate_landscape_wfc(characters=characters, connections=connections4, size0=size0, size1=size1)
    plot_landscape(landscape=landscape, characters=info)
    # print("foo")
    #run1()

    
    # size0 = 4
    # size1 = 5
    # foo = [[["Water", "Grass"] for _ in range(size0)] for _2 in range(size1)]
    # foo[1][2].remove("Water")
    # print(foo)

    # size = 4
    # characters = {
    #     'Grass': [0,1,0,1],
    #     'Water': [0,0,1,1],
    # }
    # generate_landscape_wfc(characters=characters, size=size)




if __name__ == '__main__':
    main()
