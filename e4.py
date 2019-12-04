from operator import ge, eq
from collections import Counter

inp = "372304-847060"


def has_doubles(s, strict=False):
    op = eq if strict else ge
    return any([True for c in Counter(s).values() if op(c, 2)])


def in_range(v):
    return int(inp.split('-')[0]) <= v <= int(inp.split('-')[1])


def is_valid(s, strict=False):
    return has_doubles(s, strict) and in_range(int(s))


def valid_nums(strict):
    return [s
            for a in range(10)
            for b in range(a, 10)
            for c in range(b, 10)
            for d in range(c, 10)
            for e in range(d, 10)
            for f in range(e, 10)
            if(s:=str(a)+str(b)+str(c)+str(d)+str(e)+str(f)) and is_valid(s, strict)]


# 1 and 2
print(len(valid_nums(False)))
print(len(valid_nums(True)))
