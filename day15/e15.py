from computer import Computer
from copy import deepcopy
from collections import defaultdict
import sys
from pos import Pos


N = 1
S = 2
W = 3
E = 4

UNEXPLORED = -1
WALL = 0
CLEAR = 1
OXYGEN = 2
BOT = 3


def to_asci(i):
    if i == UNEXPLORED:
        return "?"
    if i == WALL:
        return "#"
    if i == CLEAR:
        return " "
    if i == OXYGEN:
        return "O"
    if i == BOT:
        return "D"


def print_map(world, bot_pos):
    world = deepcopy(world)
    world[bot_pos] = BOT
    min_x = min([pos.x for pos in world.keys()])
    min_y = min([pos.y for pos in world.keys()])
    max_x = max([pos.x for pos in world.keys()])
    max_y = max([pos.y for pos in world.keys()])

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            v = world[x, y] if (x, y) in world else -1
            print(to_asci(v), end=" ")
        print()


def pos_to_move(from_pos, to_pos):
    if to_pos == from_pos.east:
        return E
    elif to_pos == from_pos.west:
        return W
    elif to_pos == from_pos.south:
        return S
    elif to_pos == from_pos.north:
        return N
    else:
        print(from_pos, to_pos)
        raise Exception("Can only compare neighbouring positions")


class Droid:
    def __init__(self, computer, start_pos=Pos(0, 0)):
        self.start_pos = start_pos
        self.cur_pos = start_pos
        self.world = defaultdict(lambda: UNEXPLORED)
        self.world[self.cur_pos] = CLEAR
        self.computer = computer

    def find_oxygen(self):
        self.explore_world()
        return self._make_plan(self.start_pos, OXYGEN)

    def explore_world(self):
        while path := self._make_plan(self.cur_pos):
            self._execute_plan(path)

    # Find closest available goal position
    def _make_plan(self, from_pos, goal=UNEXPLORED):
        frontier = [(n, []) for n in from_pos.neighbours if self.world[n] != WALL]
        explored = set()

        while frontier:
            pos, path = frontier.pop(0)
            explored.add(pos)
            if self.world[pos] == goal:
                return path + [pos]

            for neighbour_pos in pos.neighbours:
                if self.world[neighbour_pos] != WALL and neighbour_pos not in explored:
                    frontier.append((neighbour_pos, path + [pos]))
            frontier.sort(key=lambda x: len(x[1]))

    def _execute_plan(self, plan):
        while plan:
            new_pos = plan.pop(0)
            move = pos_to_move(self.cur_pos, new_pos)
            self.world[new_pos] = next(self.computer.run(move))
            if self.world[new_pos] != WALL:
                self.cur_pos = new_pos


def spread_oxygen(world, from_pos):
    frontier = [n for n in from_pos.neighbours if world[n] == CLEAR]
    minute = 0
    while frontier:
        this_round = set()
        for pos in frontier:
            world[pos] = OXYGEN
            for n in pos.neighbours:
                if world[n] == CLEAR:
                    this_round.add(n)
        frontier = list(this_round)
        minute += 1
    return minute


if __name__ == "__main__":
    with open("e15.txt") as f:
        data = list(map(int, f.read().split(",")))
    computer = Computer(data)

    droid = Droid(computer)
    plan = droid.find_oxygen()
    # 1
    print(len(plan))
    # 2
    print(spread_oxygen(droid.world, plan[-1]))
