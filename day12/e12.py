import numpy as np
import re


class MoonSimulator:
    def __init__(self, position_matrix):
        self.start_positions = np.copy(position_matrix)

    def tot_energy(self, at_step):
        self._reset()
        for _ in range(at_step):
            self._step()
        pot_energy = np.sum(np.abs(self.positions), axis=1)
        kin_energy = np.sum(np.abs(self.velocity), axis=1)
        return np.sum(pot_energy * kin_energy)

    def steps_until_repeating_universe(self):
        self._reset()
        cycles = [
            self._find_cycle(axis) for axis in range(self.start_positions.shape[1])
        ]
        return self._lcm(cycles)

    def _find_cycle(self, axis):
        self._reset()
        while True:
            self._step()
            if np.all(self.positions[:, axis] == self.start_positions[:, axis]):
                return self.steps

    def _step(self):
        changes = np.sum(self.positions[:, None, :] < self.positions[:, :], axis=1)
        changes -= np.sum(self.positions[:, None, :] > self.positions[:, :], axis=1)
        self.velocity += changes
        self.positions += self.velocity
        self.steps += 1

    def _reset(self):
        self.positions = np.copy(self.start_positions)
        self.velocity = np.zeros_like(self.positions, np.int32)
        self.steps = 1

    def _lcm(self, lst):
        return np.lcm(*lst) if len(lst) == 2 else np.lcm(lst[0], self._lcm(lst[1:]))


def parse_data(data):
    return np.array(
        [list(map(int, re.findall(r"(-?\d+)", l))) for l in data.splitlines(False)]
    )


if __name__ == "__main__":
    with open("e12.txt") as f:
        data = f.read()

    # 1
    print(MoonSimulator(parse_data(data)).tot_energy(1000))

    # 2
    print(MoonSimulator(parse_data(data)).steps_until_repeating_universe())
