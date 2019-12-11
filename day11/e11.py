import numpy as np
import matplotlib.pyplot as plt
from computer import Computer
from collections import defaultdict

BLACK = 0
WHITE = 1

LEFT = 0
RIGHT = 1

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3


class Robot:
    def __init__(self, computer, initial_direction=NORTH):
        self.brain = computer
        self.cur_direction = initial_direction
        self.cur_pos = (0, 0)
        self.painted = defaultdict(lambda: BLACK)

    def run(self, inp):
        while outputs := self._get_outputs(inp):
            color, direction = outputs
            self.painted[self.cur_pos] = color
            self._turn(direction)
            self._move_forward()
            inp = self.painted[self.cur_pos]
        return self.painted

    def _get_outputs(self, inp):
        return [v for v in self.brain.run(inp)]

    def _turn(self, direction):
        if direction == RIGHT:
            self.cur_direction = (self.cur_direction + 1) % 4
        elif direction == LEFT:
            self.cur_direction = (self.cur_direction + 3) % 4

    def _move_forward(self):
        if self.cur_direction == NORTH:
            self.cur_pos = (self.cur_pos[0], self.cur_pos[1] - 1)
        if self.cur_direction == EAST:
            self.cur_pos = (self.cur_pos[0] + 1, self.cur_pos[1])
        if self.cur_direction == SOUTH:
            self.cur_pos = (self.cur_pos[0], self.cur_pos[1] + 1)
        if self.cur_direction == WEST:
            self.cur_pos = (self.cur_pos[0] - 1, self.cur_pos[1])


def gen_image(painted):
    min_x = min([x[0] for x in painted.keys()])
    min_y = min([x[1] for x in painted.keys()])
    max_x = max([x[0] for x in painted.keys()])
    max_y = max([x[1] for x in painted.keys()])

    img = np.zeros((max_y - min_y + 1, max_x - min_x + 1))
    for k, v in painted.items():
        img[k[1] - min_y, k[0] - min_x] = v
    return img


def display_image(img):
    plt.imshow(img)
    plt.show()


if __name__ == "__main__":
    with open("e11.txt") as f:
        data = list(map(int, f.read().split(",")))

    # 1
    print(len(Robot(Computer(data)).run(0)))

    # 2
    painted = Robot(Computer(data)).run(1)
    display_image(gen_image(painted))
