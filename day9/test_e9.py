from e9 import Computer


def test_pos_mode():
    # eq
    assert next(Computer([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]).run(7)) == 0
    assert next(Computer([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]).run(8)) == 1
    assert next(Computer([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]).run(9)) == 0
    # lt
    assert next(Computer([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]).run(7)) == 1
    assert next(Computer([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]).run(8)) == 0
    assert next(Computer([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]).run(9)) == 0


def test_im_mode():
    # eq
    assert next(Computer([3, 3, 1108, -1, 8, 3, 4, 3, 99]).run(7)) == 0
    assert next(Computer([3, 3, 1108, -1, 8, 3, 4, 3, 99]).run(8)) == 1
    assert next(Computer([3, 3, 1108, -1, 8, 3, 4, 3, 99]).run(9)) == 0
    # lt
    assert next(Computer([3, 3, 1107, -1, 8, 3, 4, 3, 99]).run(7)) == 1
    assert next(Computer([3, 3, 1107, -1, 8, 3, 4, 3, 99]).run(8)) == 0
    assert next(Computer([3, 3, 1107, -1, 8, 3, 4, 3, 99]).run(9)) == 0


def test_quine():
    data = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    assert list(Computer(data).run(1)) == data


def test_basic():
    data = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    assert len(str(next(Computer(data).run(1)))) == 16
    data = [104, 1125899906842624, 99]
    assert next(Computer(data).run(1)) == data[1]


def test_solution():
    with open("e9.txt") as f:
        data = list(map(int, f.read().split(",")))
    assert next(Computer(data).run(1)) == 2171728567
    assert next(Computer(data).run(2)) == 49815
