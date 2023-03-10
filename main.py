import matplotlib.pyplot as plt
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

def generate_landscape(characters, size):
    landscape = np.random.choice(characters, size*size).reshape(size,size)
    return landscape


# def plot_landscape(landscape,cmap):

#     plt.imshow(landscape, cmap, rasterized=True)
#     plt.show()



def main():
    size = 10
    characters = ['L', 'W', 'S']


    landscape = generate_landscape(characters=characters, size=size)
    
    codes = {'L': 0,'W':1,'S':2}
    values = np.vectorize(codes.get)(landscape)

    colors = np.array([[0,1,0,1],[0,0,1,1],[1,1,0,1]])
    cmap = ListedColormap(colors)
    print(colors)
    
    plt.imshow(values, cmap, rasterized=True,vmin=0, vmax=2)
    plt.show()


if __name__ == '__main__':
    main()
