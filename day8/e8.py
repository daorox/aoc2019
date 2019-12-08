from copy import deepcopy
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

BLACK = 0
WHITE = 1
TRANSPARENT = 2

def get_checksum(data,w,h):
    layers = [data[i:i+w*h] for i in range(0, len(data), w*h)]
    min_layer = min(layers, key=lambda x: x.count(BLACK))
    return Counter(min_layer)[WHITE]*Counter(min_layer)[TRANSPARENT]

def get_image(data,w,h):
    layers = np.array(data).reshape(-1,h*w)
    non_trans_mask = (layers != TRANSPARENT).argmax(0)
    return layers[non_trans_mask, np.arange(w*h)].reshape(h,w)

def display_image(img):
    plt.imshow(img)
    plt.show()

if __name__ == "__main__":
    with open("e8.txt") as f:
        data = list(map(int, f.read().rstrip()))
    w = 25
    h = 6
    #1
    print(get_checksum(data, w,h))
    #2
    display_image(get_image(data,w,h))
