import numpy as np
from copy import deepcopy


def dist(a, b):
    return np.sqrt(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2))


def angle(ast, origo):
    v1 = np.array([0, -1])
    v2 = np.array([ast[0] - origo[0], ast[1] - origo[1]])

    cosine_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    ang = round(np.arccos(cosine_angle), 6)
    return 2 * np.pi - ang if ast[0] < origo[0] else ang


def get_reachable(sts, o):
    return {
        angle(a, o): a
        for a in sorted(sts, key=lambda x: dist(x, o), reverse=True)
        if a is not o
    }


def find_best_asteroid(astrs):
    return max(((a, get_reachable(astrs, a)) for a in astrs), key=lambda x: len(x[1]))


def get_vaporization_order(asteroids):
    asteroids = deepcopy(asteroids)
    vaporized = []
    best_astr = find_best_asteroid(asteroids)[0]
    while asteroids != set([best_astr]):
        reachable = [x[1] for x in sorted(get_reachable(asteroids, best_astr).items())]
        vaporized.extend(reachable)
        asteroids.difference_update(set(reachable))
    return vaporized


def get_asteroids(data):
    return {(x, y) for y, l in enumerate(data) for x, c in enumerate(l) if c == "#"}


if __name__ == "__main__":
    with open("e10.txt") as f:
        asteroids = get_asteroids([line.rstrip() for line in f])

    # 1
    print(len(find_best_asteroid(asteroids)[1]))

    # 2
    print(get_vaporization_order(asteroids)[199])
