from operator import add, mul
from copy import deepcopy

# 1


def parse_opcodes(lst):
    lst = deepcopy(lst)
    for i in range(0, len(lst), 4):
        a = lst[lst[i + 1]]
        b = lst[lst[i + 2]]
        op = add if lst[i] == 1 else mul
        lst[lst[i + 3]] = op(a, b)

        if lst[i + 4] == 99:
            break
    return lst[0]


with open("e2.txt") as f:
    lst = list(map(int, f.read().split(",")))

lst[1] = 12
lst[2] = 2

print(parse_opcodes(lst))

# 2

with open("e2.txt") as f:
    lst = list(map(int, f.read().split(",")))
for x in range(100):
    for y in range(100):
        lst[1] = x
        lst[2] = y

        if parse_opcodes(lst) == 19690720:
            print(x, y)
