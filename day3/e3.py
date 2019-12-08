with open("e3.txt") as f:
    lines = f.read().splitlines()

all_pos_costs = []
for line in lines:
    pos = (0, 0)
    steps = 0
    # The amount of steps required to reach each position
    pos_cost = {}
    for cell in line.split(","):
        d = cell[0]
        length = int(cell[1:])
        if d == "R":
            new_positions = zip(
                (pos[0] + x for x in range(1, length + 1)), [pos[1]] * length
            )
        if d == "U":
            new_positions = zip(
                [pos[0]] * length, (pos[1] - x for x in range(1, length + 1))
            )
        if d == "L":
            new_positions = zip(
                (pos[0] - x for x in range(1, length + 1)), [pos[1]] * length
            )
        if d == "D":
            new_positions = zip(
                [pos[0]] * length, (pos[1] + x for x in range(1, length + 1))
            )
        for new_pos in new_positions:
            steps += 1
            if new_pos not in pos_cost:
                pos_cost[new_pos] = steps
        pos = new_pos
    all_pos_costs.append(pos_cost)


def dist(x_value, x_goal, y_value, y_goal):
    return abs(x_value - x_goal) + abs(y_value - y_goal)


all_coords = [set(line.keys()) for line in all_pos_costs]

# 1
print(min(dist(i[0], 0, i[1], 0) for i in all_coords[0].intersection(all_coords[1])))
# 2
print(
    min(
        all_pos_costs[0][i] + all_pos_costs[1][i]
        for i in all_coords[0].intersection(all_coords[1])
    )
)
