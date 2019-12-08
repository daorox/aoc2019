# 1
with open("e1.txt") as f:
    print(sum(x // 3 - 2 for x in map(int, f.readlines())))

# 2


def calc_extras(given):
    extra_cost = given // 3 - 2
    tot = 0
    while extra_cost > 0:
        tot += extra_cost
        extra_cost = extra_cost // 3 - 2
    return tot


with open("e1.txt") as f:
    print(sum(x // 3 - 2 + calc_extras(x // 3 - 2) for x in map(int, f.readlines())))
