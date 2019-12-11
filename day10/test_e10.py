from e10 import get_asteroids, find_best_asteroid, get_vaporization_order
from math import pi

SMALL_CONST = 0.00001

best1 = (
    (3, 4),
    8,
    """.#..#
.....
#####
....#
...##""",
)

best2 = (
    (5, 8),
    33,
    """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####""",
)

best3 = (
    (1, 2),
    35,
    """#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.""",
)

best4 = (
    (6, 3),
    41,
    """.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..""",
)

best5 = (
    (11, 13),
    210,
    """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""",
)

best5_vaporizaiton_order = {
    1: (11, 12),
    2: (12, 1),
    3: (12, 2),
    10: (12, 8),
    20: (16, 0),
    50: (16, 9),
    100: (10, 16),
    199: (9, 6),
    200: (8, 2),
    201: (10, 9),
    299: (11, 1),
}


def split_lines(data):
    return [line.rstrip() for line in data.splitlines()]


def test_finding_best():
    for test in [best1, best2, best3, best4, best5]:
        astr, reachable_count, data = test
        asteroids = get_asteroids(split_lines(data))
        res = find_best_asteroid(asteroids)
        assert res[0] == astr
        assert len(res[1]) == reachable_count


def test_finding_best_real():
    with open("e10.txt") as f:
        data = [line.rstrip() for line in f]

    reachable_count = 326

    asteroids = get_asteroids(data)
    res = find_best_asteroid(asteroids)

    assert len(res[1]) == reachable_count


def test_vaporization_order():
    astr, reachable_count, data = best5
    asteroids = get_asteroids(split_lines(data))
    vaporized = get_vaporization_order(asteroids)
    for idx, ast in best5_vaporizaiton_order.items():
        assert vaporized[idx - 1] == ast


def test_vaporization_real():
    with open("e10.txt") as f:
        data = [line.rstrip() for line in f]

    asteroids = get_asteroids(data)
    vaporized = get_vaporization_order(asteroids)

    assert vaporized[199][0] * 100 + vaporized[199][1] == 1623
