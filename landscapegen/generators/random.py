import random

import numpy as np


def generate_random(characters, size0, size1):
    possibilities = [[characters for _1 in range(size0)] for _2 in range(size1)]
    choice = [
        [random.choice(subsublist) for subsublist in sublist]
        for sublist in possibilities
    ]
    landscape = np.array(choice)
    # landscape = np.random.choice(characters, size0*size1).reshape(size0,size1)
    return landscape
