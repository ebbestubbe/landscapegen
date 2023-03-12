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


def generate_landscape_wfc(characters, size0, size1):

    #rules:
    connections = {
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

    wavefunction = [[characters for _1 in range(size0)] for _2 in range(size1)]
    undetermined = [[len(subsublist)!=1 for subsublist in sublist] for sublist in wavefunction]
    coords = [[(j,i) for i,subsublist in enumerate(sublist) if undetermined[j][i]] for j,sublist in enumerate(wavefunction)]
    flat_coords = [item for sublist in coords for item in sublist]
    point = random.choice(flat_coords)
    random_x = point[0]
    random_y = point[1]

    #Now we have a random point that we can choose to do something with:
    # Assume that any choice is valid
    # Pick random tile
    # Visit neighbors, remove tiles that are not valid
    


    # for i in landscape.shape[0]:
    #     for j in landscape.shape[1]:
    #         neighbor_0 = landscape[i-1,j]
    #         neighbor_1 = landscape[i,j+1]
    #         neighbor_2 = landscape[i+1,j]
    #         neighbor_3 = landscape[i,j-1]



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
    size0 = 4
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
    depth_first_grid()
    # size0 = 2
    # size1 = 3
    # info = {
    #     'Grass': [0,1,0,1],
    #     'Water': [0,0,1,1],
    #     'Sand': [1,1,0,1],
    # }
    # characters=list(info.keys())
    # generate_landscape_wfc(characters=characters, size0=size0, size1=size1)

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
