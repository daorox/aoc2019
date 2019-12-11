from e11 import Robot
from computer import Computer


def test_robot():
    with open("e11.txt") as f:
        data = list(map(int, f.read().split(",")))
    assert len(Robot(Computer(data)).run(0)) == 1747
