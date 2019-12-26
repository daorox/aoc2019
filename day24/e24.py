import numpy as np
from scipy.signal import convolve2d


class BugEmulator:
    """Expects a 2d world"""

    def __init__(self, world):
        self.world = world
        self.seen_worlds = set()

    def step_until_repeating_world(self):
        while self.world.tobytes() not in self.seen_worlds:
            self.seen_worlds.add(self.world.tobytes())
            self.step()

    def step(self):
        new_world = np.copy(self.world)
        local_bugs = self.count_buggy_neighbours(self.world)
        new_world[(self.world == 1) & (local_bugs != 1)] = 0
        new_world[(self.world == 0) & ((local_bugs == 1) | (local_bugs == 2))] = 1
        self.world = new_world

    def count_buggy_neighbours(self, world_level):
        kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
        return convolve2d(world_level, kernel, mode="same")

    @property
    def biodiversity(self):
        vector_world = self.world.reshape(-1)
        return np.sum(vector_world * 2 ** np.arange(len(vector_world)))


class BugEmulatorRecursive:
    """Expects a 3d world"""

    def __init__(self, world, start_level):
        self.cur_min_level = start_level - 1
        self.cur_max_level = start_level + 1
        self.world = world

    def do_steps(self, amount):
        for _ in range(amount):
            self.step()

    def step(self):
        new_world = np.copy(self.world)
        for level in range(self.cur_min_level, self.cur_max_level + 1):
            local_bugs = self.count_buggy_neighbours(self.world[level])
            for i in range(self.world.shape[-2]):
                for j in range(self.world.shape[-1]):
                    if i == 2 and j == 2:
                        continue
                    bugs = local_bugs[i, j]

                    bugs += self.count_outer_bugs(self.world[level - 1], i, j)
                    bugs += self.count_inner_bugs(self.world[level + 1], i, j)

                    if self.world[level, i, j] and bugs != 1:
                        new_world[level, i, j] = 0
                    elif not self.world[level, i, j] and (bugs == 1 or bugs == 2):
                        new_world[level, i, j] = 1

                    if level == self.cur_min_level and bugs:
                        self.cur_min_level -= 1
                    if level == self.cur_max_level and bugs:
                        self.cur_max_level += 1

        self.world = new_world

    def count_buggy_neighbours(self, world_level):
        kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
        return convolve2d(world_level, kernel, mode="same")

    def count_inner_bugs(self, world_level, i, j):
        bugs = 0
        if i == 1 and j == 2:
            bugs += np.sum(world_level[0, :])
        if i == 3 and j == 2:
            bugs += np.sum(world_level[world_level.shape[-1] - 1, :])
        if i == 2 and j == 1:
            bugs += np.sum(world_level[:, 0])
        if i == 2 and j == 3:
            bugs += np.sum(world_level[:, world_level.shape[-2] - 1])
        return bugs

    def count_outer_bugs(self, world_level, i, j):
        bugs = 0
        if i == 0:
            bugs += world_level[1, 2]
        if i == world_level.shape[-2] - 1:
            bugs += world_level[3, 2]
        if j == 0:
            bugs += world_level[2, 1]
        if j == world_level.shape[-1] - 1:
            bugs += world_level[2, 3]
        return bugs


def create_world(ascii_data, max_level, start_level):
    BUG = "#"
    start_grid = np.array(
        [[int(c == BUG) for c in row] for row in ascii_data.splitlines(False)],
        dtype=np.int,
    )
    world = np.zeros((max_level, *start_grid.shape), dtype=np.int)
    world[start_level] = start_grid
    return world


def solve1(ascii_data):
    BUG = "#"
    world = np.array(
        [[int(c == BUG) for c in row] for row in ascii_data.splitlines(False)],
        dtype=np.int,
    )
    b = BugEmulator(world)
    b.step_until_repeating_world()
    return b.biodiversity


def solve2(data):
    minutes = 200
    max_level = minutes * 2 + 1
    start_level = max_level // 2
    world = create_world(data, max_level, start_level)

    b = BugEmulatorRecursive(world, start_level)
    b.do_steps(minutes)
    return np.sum(b.world)


if __name__ == "__main__":
    with open("e24.txt") as f:
        data = f.read()
    # 1
    print(solve1(data))
    # 2
    print(solve2(data))
