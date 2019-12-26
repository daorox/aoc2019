from computer import Computer


def to_ascii(cmd):
    return [ord(c) for c in cmd + "\n"]


def automated_play(data):
    # TODO complete this
    pass


def manual_play(data):
    computer = Computer(data)

    cmd = ""
    while True:
        for x in computer.run(to_ascii(cmd)):
            print(chr(x), end="")
        cmd = input()


if __name__ == "__main__":
    with open("e25.txt") as f:
        data = list(map(int, f.read().split(",")))
    manual_play(data)
