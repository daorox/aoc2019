from computer import Computer

with open("e21.txt") as f:
    data = list(map(int, f.read().split(",")))


def to_ascii(lsts):
    return [ord(c) for lst in lsts for c in lst + "\n"]


def run_cmds(cmds):
    for x in Computer(data).run(cmds):
        try:
            print(chr(x), end="")
        except ValueError:
            return x


if __name__ == "__main__":
    # A
    cmds = ["NOT A J", "NOT B T", "OR T J", "NOT C T", "OR T J", "AND D J", "WALK"]
    print(run_cmds(to_ascii(cmds)))

    # B
    cmds = [
        "NOT A J",
        "NOT B T",
        "OR T J",
        "NOT C T",
        "OR T J",
        "AND D J",
        "AND E T",
        "OR H T",
        "AND T J",
        "RUN",
    ]
    print(run_cmds(to_ascii(cmds)))
