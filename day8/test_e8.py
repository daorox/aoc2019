from e8 import get_checksum, get_image
import numpy as np

def test_checksum():
    data = [int(c) for c in "123456789012"]
    assert get_checksum(data,3,2) == 1

    with open("e8.txt") as f:
        data = list(map(int, f.read().rstrip()))
    assert get_checksum(data,25,6) == 1548

def test_get_image():
    data = [int(c) for c in "0222112222120000"]
    assert np.all(get_image(data,2,2).reshape(-1) == np.array([0,1,1,0]))
