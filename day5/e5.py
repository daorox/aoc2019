from copy import deepcopy


def get_action(instruction):
    s = str(instruction)

    # Single digit op without params
    if len(s) == 1:
        return int(s), None

    op, remaining = s[-2:], s[:-2]

    if len(remaining) == 0:
        return int(op), None

    if len(remaining) == 1:
        return int(op), (int(remaining[-1]), 0, 0)
    if len(remaining) == 2:
        return int(op), (int(remaining[-1]), int(remaining[-2]), 0)
    if len(remaining) == 3:
        return int(op), (int(remaining[-1]), int(remaining[-2]), int(remaining[-3]))


def get_params(lst, cur_pos, count, modes):
    return [lst[cur_pos+i+1] if modes and modes[i] else lst[lst[cur_pos+i+1]] for i in range(count)]


def parse_opcodes(lst):
    lst = deepcopy(lst)
    i = 0
    while True:
        op, modes = get_action(lst[i])

        if op == 1:
            a, b = get_params(lst, i, 2, modes)
            lst[lst[i+3]] = a + b
            i += 4
        elif op == 2:
            a, b = get_params(lst, i, 2, modes)
            lst[lst[i+3]] = a * b
            i += 4
        elif op == 3:
            lst[lst[i+1]] = INPUT
            i += 2
        elif op == 4:
            print(*get_params(lst, i, 1, modes))
            i += 2
        elif op == 5:
            a, b = get_params(lst, i, 2, modes)
            i = b if a != 0 else i + 3
        elif op == 6:
            a, b = get_params(lst, i, 2, modes)
            i = b if a == 0 else i + 3
        elif op == 7:
            a, b = get_params(lst, i, 2, modes)
            lst[lst[i+3]] = 1 if a < b else 0
            i += 4
        elif op == 8:
            a, b = get_params(lst, i, 2, modes)
            lst[lst[i+3]] = 1 if a == b else 0
            i += 4
        elif op == 99:
            break

    return lst[0]


with open("e5.txt") as f:
    lst = list(map(int, f.read().split(",")))

# 1
INPUT = 1
parse_opcodes(lst)
# 2
INPUT = 5
parse_opcodes(lst)
