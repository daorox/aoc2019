from collections import defaultdict


def get_mappings(data):
    orbiting = {}
    for line in data:
        a, b = line.split(")")
        if a not in orbiting:
            orbiting[a] = None

        orbiting[b] = a

    orbited = defaultdict(list)
    for k, v in orbiting.items():
        if v:
            orbited[v].append(k)
    return orbiting, orbited


class Orbits:
    def __init__(self, orbiting_map, orbited_map):
        self.orbiting, self.orbited = orbiting_map, orbited_map

    def count_orbits(self):
        count = 0
        print(self.orbiting)
        for val in self.orbiting.values():
            orbited = val
            while orbited:
                count += 1
                orbited = self.orbiting[orbited]
        return count

    def count_orbital_transfers(self, start, end):
        explored = set()
        frontier = [(self.orbiting[start], 1), *[(orb, 1)
                                                 for orb in self.orbited[start]]]
        while frontier:
            frontier = sorted(frontier, key=lambda x: x[1])
            orb, cost = frontier.pop(0)
            explored.add(orb)

            if orb == end:
                return cost-2

            if orb in self.orbiting and self.orbiting[orb] not in explored:
                frontier.append((self.orbiting[orb], cost+1))

            if orb in self.orbited:
                for out in self.orbited[orb]:
                    if out not in explored:
                        frontier.append((out, cost+1))
        return -1


if __name__ == "__main__":
    with open("e6.txt") as f:
        lines = list(x.rstrip() for x in f.readlines())
    orbiting, orbited = get_mappings(lines)

    solver = Orbits(orbiting, orbited)
    print(solver.count_orbits())
    print(solver.count_orbital_transfers("YOU", "SAN"))
