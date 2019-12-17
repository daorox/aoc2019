import numpy as np


def keep_one(i):
    return abs(i) % 10


def apply_phases(data, pattern_new, repeats):
    data_pattern_ratio = int(((len(data) / len(pattern_new)) + 1))

    if repeats > 1:
        pattern_new = np.repeat(pattern_new, repeats)

    tiled = np.tile(pattern_new, data_pattern_ratio)
    tiled = tiled[1 : len(data) + 1]
    tiled = np.resize(tiled, data.shape)

    return keep_one(np.sum(data * tiled))


def part1(data):
    COUNT = 100
    phases = np.array([0, 1, 0, -1])
    for _ in range(COUNT):
        new_arr = np.zeros_like(data)
        for i in range(len(data)):
            new_arr[i] = apply_phases(data, phases, i + 1)
        data = np.array(new_arr)
    return data


def part2(data):
    offset = int("".join(map(str, data[:7].tolist())))
    remaining = len(data) - offset
    data = data[offset:]
    data = np.resize(data, remaining)

    COUNT = 100
    for _ in range(COUNT):
        new_arr = np.zeros_like(data)
        tot = np.sum(data)
        for i in range(remaining):
            new_arr[i] = keep_one(tot)
            tot -= data[i]
        data = new_arr
    return data


if __name__ == "__main__":
    with open("e16.txt") as f:
        raw_data = f.read()[:-1]

    data = np.array(list(map(int, list(raw_data))))
    # # 1
    print("".join(map(str, part1(data)[:8])))
    # 2
    data = np.array(list(map(int, list(raw_data * 10_000))))
    print("".join(map(str, part2(data)[:8])))

