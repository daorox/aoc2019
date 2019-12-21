import string
from collections import defaultdict
from pos import Pos

CLEAR = "."


class PortalParser:
    def __init__(self, world):
        self.portals = self._find_portals(world)
        self.start = self.portals[("A", "A")][0]
        self.goal = self.portals[("Z", "Z")][0]
        self._create_portal_lookups()

    def _find_portals(self, world):
        portals = defaultdict(list)
        for i, line in enumerate(world[2:]):
            for j, c in enumerate(line[2:]):
                c = world[i][j]
                n2 = world[i - 2][j]
                n1 = world[i - 1][j]

                e2 = world[i][j + 2]
                e1 = world[i][j + 1]

                s2 = world[i + 2][j]
                s1 = world[i + 1][j]

                w2 = world[i][j - 2]
                w1 = world[i][j - 1]

                if (
                    self._is_portal_label(n1)
                    and self._is_portal_label(n2)
                    and c is CLEAR
                ):
                    portals[(n2, n1)].append(Pos(j, i))

                if (
                    self._is_portal_label(e1)
                    and self._is_portal_label(e2)
                    and c is CLEAR
                ):
                    portals[(e1, e2)].append(Pos(j, i))

                if (
                    self._is_portal_label(s1)
                    and self._is_portal_label(s2)
                    and c is CLEAR
                ):
                    portals[(s1, s2)].append(Pos(j, i))

                if (
                    self._is_portal_label(w1)
                    and self._is_portal_label(w2)
                    and c is CLEAR
                ):
                    portals[(w2, w1)].append(Pos(j, i))
        return portals

    def _create_portal_lookups(self):
        tele_dict = {}
        for v in self.portals.values():
            if len(v) is 2:
                a, b = v
                tele_dict[a] = b
                tele_dict[b] = a

        self.outer_portals = {}
        self.inner_portals = {}
        for key, value in tele_dict.items():
            if (
                key.x is 2
                or key.y is 2
                or key.x is len(world[0]) - 3
                or key.y is len(world) - 3
            ):
                self.outer_portals[key] = value
            else:
                self.inner_portals[key] = value

    def _is_portal_label(self, c):
        return c in string.ascii_uppercase


class MazeExplorer:
    def __init__(self, world, use_levels=True):
        self.world = world
        portals = PortalParser(world)
        self.inner_portals = portals.inner_portals
        self.outer_portals = portals.outer_portals
        self.start_pos = portals.start
        self.goal_pos = portals.goal
        self.use_levels = int(use_levels)

    def get_min_cost(self):
        # Cost, level, pos
        frontier = [
            (0, 0, n_pos)
            for n_pos in self.start_pos.neighbours
            if self._is_explorable(n_pos, 0)
        ]

        explored = set((self.start_pos, 0))
        while frontier:
            cost, level, pos = frontier.pop()
            if (pos, level) in explored:
                continue
            explored.add((pos, level))

            new_pos, new_level = self._teleport_if_portal(pos, level)
            cost = cost + 1 if new_pos is pos else cost + 2

            if new_pos == self.goal_pos and new_level == 0:
                return cost

            for n_pos in new_pos.neighbours:
                if (
                    self._is_explorable(n_pos, new_level)
                    and (n_pos, new_level) not in explored
                ):
                    frontier.append((cost, new_level, n_pos))
            frontier.sort(key=lambda x: x[1], reverse=True)

    def _teleport_if_portal(self, to_pos, cur_level):
        if to_pos in self.inner_portals:
            return self.inner_portals[to_pos], cur_level + self.use_levels

        if cur_level > 0:
            if to_pos in self.outer_portals:
                return self.outer_portals[to_pos], cur_level - self.use_levels

        return to_pos, cur_level

    def _is_explorable(self, pos, level):
        if at_pos(world, pos) is not CLEAR:
            return False
        if level is 0:
            if pos == self.start_pos or pos == self.goal_pos:
                return True
            if pos in self.outer_portals:
                return False
        else:
            if pos == self.start_pos or pos == self.goal_pos:
                return False
        return True


def at_pos(world, pos):
    return world[pos.y][pos.x]


if __name__ == "__main__":
    with open("e20.txt") as f:
        data = f.read()

    world = [[c for c in line] for line in data.splitlines(False)]

    # 1
    print(MazeExplorer(world, False).get_min_cost())
    # 2
    print(MazeExplorer(world).get_min_cost())
