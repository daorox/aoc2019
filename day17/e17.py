from computer import Computer
import numpy as np
import math
from enum import Enum
from dataclasses import dataclass
from scipy.signal import convolve2d

SCAFFOLD = ord("#")
EMPTY = ord(".")
NEW_LINE = ord("\n")


@dataclass
class Coord:
    i: int
    j: int

    @property
    def north(self):
        return Coord(self.i - 1, self.j)

    @property
    def east(self):
        return Coord(self.i, self.j + 1)

    @property
    def south(self):
        return Coord(self.i + 1, self.j)

    @property
    def west(self):
        return Coord(self.i, self.j - 1)

    def distance_to(self, coord):
        return abs(self.i - coord.i) + abs(self.j - coord.j)

    def to_tuple(self):
        return self.i, self.j


class Orientation(Enum):
    NORTH = ord("^")
    EAST = ord(">")
    SOUTH = ord("<")
    WEST = ord("v")


@dataclass
class Bot:
    pos: Coord
    orientation: Orientation


def parse_data(data):
    world = [[]]
    computer = Computer(data)
    for out in computer.run(data):
        if out == NEW_LINE:
            world.append([])
        elif out == EMPTY:
            world[-1].append(0)
        elif out == SCAFFOLD:
            world[-1].append(1)
        else:
            # Bot
            world[-1].append(1)
            j = len(world[-1]) - 1
            i = len(world) - 1
            pos = Coord(i, j)
            bot = Bot(pos, Orientation(out))

    return np.array(world[:-2]), bot


def is_valid(world, coord):
    height, width = world.shape
    return 0 <= coord.i < height and 0 <= coord.j < width


def get_neighbour(pos, int_orientation):
    if int_orientation == 0:
        return pos.north
    if int_orientation == 1:
        return pos.east
    if int_orientation == 2:
        return pos.south
    if int_orientation == 3:
        return pos.west

def next_move(world, bot):
    # TODO refactor this monster
    if bot.orientation == Orientation.NORTH:
        if world[bot.pos.west.to_tuple()]:
            new_pos = bot.pos.west
            while is_valid(world, new_pos) and world[new_pos.to_tuple()]:
                new_pos = new_pos.west
            new_pos = new_pos.east
            return f"L{new_pos.distance_to(bot.pos)}", Bot(new_pos, Orientation.WEST)
        elif world[bot.pos.east.to_tuple()]:
            new_pos = bot.pos.east
            while is_valid(world, new_pos) and world[new_pos.to_tuple()]:
                new_pos = new_pos.east
            new_pos = new_pos.west
            return f"R{new_pos.distance_to(bot.pos)}", Bot(new_pos, Orientation.EAST)
    elif bot.orientation == Orientation.EAST:
        if world[bot.pos.north.to_tuple()]:
            new_pos = bot.pos.north
            while is_valid(world, new_pos) and world[new_pos.to_tuple()]:
                new_pos = new_pos.north
            new_pos = new_pos.south
            return f"L{new_pos.distance_to(bot.pos)}", Bot(new_pos, Orientation.NORTH)
        elif world[bot.pos.south.to_tuple()]:
            new_pos = bot.pos.south
            while is_valid(world, new_pos) and world[new_pos.to_tuple()]:
                new_pos = new_pos.south
            new_pos = new_pos.north
            return f"R{new_pos.distance_to(bot.pos)}", Bot(new_pos, Orientation.SOUTH)
    elif bot.orientation == Orientation.SOUTH:
        if world[bot.pos.east.to_tuple()]:
            new_pos = bot.pos.east
            while is_valid(world, new_pos) and world[new_pos.to_tuple()]:
                new_pos = new_pos.east
            new_pos = new_pos.west
            return f"L{new_pos.distance_to(bot.pos)}", Bot(new_pos, Orientation.EAST)
        elif world[bot.pos.west.to_tuple()]:
            new_pos = bot.pos.west
            while is_valid(world, new_pos) and world[new_pos.to_tuple()]:
                new_pos = new_pos.west
            new_pos = new_pos.east
            return f"R{new_pos.distance_to(bot.pos)}", Bot(new_pos, Orientation.WEST)
    elif bot.orientation == Orientation.WEST:
        if world[bot.pos.north.to_tuple()]:
            new_pos = bot.pos.north
            while is_valid(world, new_pos) and world[new_pos.to_tuple()]:
                new_pos = new_pos.north
            new_pos = new_pos.south
            return f"R{new_pos.distance_to(bot.pos)}", Bot(new_pos, Orientation.NORTH)
        elif world[bot.pos.south.to_tuple()]:
            new_pos = bot.pos.south
            while is_valid(world, new_pos) and world[new_pos.to_tuple()]:
                new_pos = new_pos.south
            new_pos = new_pos.north
            return f"L{new_pos.distance_to(bot.pos)}", Bot(new_pos, Orientation.SOUTH)


def find_sequence(world, bot):
    seqs = []
    while move := next_move(world, bot):
        seq, bot = move
        seqs.append(seq)
    return seqs


def occurence_count(seq, sub_seq):
    seq_str = ",".join(seq)
    sub_seq_str = ",".join(sub_seq)
    return seq_str.count(sub_seq_str)


def exclude(seq, sub_seq):
    seq_str = ",".join(seq)
    sub_seq_str = ",".join(sub_seq)
    return [x for x in seq_str.replace(sub_seq_str, "").split(",") if x]


# Find a long recurring subsequence, remove it from sequence
# repeat. Backtrack if necessary.
def find_groups(seq, depth=1):
    MAX_GROUP_COUNT = 3
    MAX_SEQ_LENGTH = 20
    if seq == []:
        return []
    if depth > MAX_GROUP_COUNT:
        raise Exception
    start_seq = seq[:MAX_SEQ_LENGTH]
    while len(",".join(start_seq)) > MAX_SEQ_LENGTH:
        start_seq = start_seq[:-1]
    # Assumes sequence occurs at least twice
    while True:
        if occurence_count(seq, start_seq) < 2:
            start_seq = start_seq[:-1]
        else:
            try:
                # Simply removing the sub sequence is not bullet proof as it may generate
                # patterns that are too long, but it works for the given input data
                other_seqs = find_groups(exclude(seq, start_seq), depth + 1)
                return [start_seq] + other_seqs
            except:
                start_seq = start_seq[:-1]
                if not start_seq:
                    raise Exception


def group_sequences(seq, groups):
    # Assumes seq can be grouped perfectly using groups
    # and that no group is a subset of another group
    ret = []
    while seq:
        for i, group in enumerate(groups):
            if len(group) <= len(seq) and seq[: len(group)] == group:
                ret.append(chr(ord("A") + i))
                seq = seq[len(group) :]
    return ret


def to_input_format(main_routine, functions):
    main_str = ",".join(main_routine)
    func_str = "\n".join(
        [",".join([f"{c[0]},{c[1:]}" for c in func]) for func in functions]
    )
    joined = "\n".join([main_str, func_str, "n\n"])
    return [ord(c) for c in joined]


def get_dust(computer, computer_input):
    for x in computer.run(computer_input):
        continue
    return x


def solve1(world):
    kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    intersections = convolve2d(world, kernel, mode="same") == 5
    indices = np.argwhere(intersections)
    return np.sum(indices[:, 0] * indices[:, 1])


def solve2(world, bot):
    computer = Computer(data)
    computer.mem[0] = 2

    seq = find_sequence(world, bot)
    functions = find_groups(seq)
    main_routine = group_sequences(seq, functions)
    computer_input = to_input_format(main_routine, functions)
    return get_dust(computer, computer_input)


if __name__ == "__main__":
    with open("e17.txt") as f:
        data = list(map(int, f.read().split(",")))
    world, bot = parse_data(data)
    # 1
    print(solve1(world))
    # 2
    print(solve2(world, bot))
