import matplotlib.pyplot as plt
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


def generate_landscape(characters, size):
    landscape = np.random.choice(characters, size*size).reshape(size,size)
    return landscape


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


def main():
    size = 4
    characters = {
        'L': [0,1,0,1],
        'W': [0,0,1,1],
        'S': [1,1,0,1],
        "lava": [1,0,0,1]
    }
    

    landscape = generate_landscape(characters=list(characters.keys()), size=size)
    print(landscape)
    plot_landscape(landscape,characters)


if __name__ == '__main__':
    main()
