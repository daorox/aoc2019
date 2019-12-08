from e7 import Computer, AmplificationCircuit

# Tests assuring that the computer still can solve the day 5 problems
def test_pos_mode():
    # eq
    assert Computer([3,9,8,9,10,9,4,9,99,-1,8]).run(7) == 0
    assert Computer([3,9,8,9,10,9,4,9,99,-1,8]).run(8) == 1
    assert Computer([3,9,8,9,10,9,4,9,99,-1,8]).run(9) == 0
    # lt
    assert Computer([3,9,7,9,10,9,4,9,99,-1,8 ]).run(7) == 1
    assert Computer([3,9,7,9,10,9,4,9,99,-1,8 ]).run(8) == 0
    assert Computer([3,9,7,9,10,9,4,9,99,-1,8 ]).run(9) == 0


def test_im_mode():
    # eq
    assert Computer([3,3,1108,-1,8,3,4,3,99]).run(7) == 0
    assert Computer([3,3,1108,-1,8,3,4,3,99]).run(8) == 1
    assert Computer([3,3,1108,-1,8,3,4,3,99]).run(9) == 0
    # lt
    assert Computer([3,3,1107,-1,8,3,4,3,99]).run(7) == 1
    assert Computer([3,3,1107,-1,8,3,4,3,99]).run(8) == 0
    assert Computer([3,3,1107,-1,8,3,4,3,99]).run(9) == 0

def test_basic():
    data = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
    assert Computer(data).run(7) == 999
    assert Computer(data).run(8) == 1000
    assert Computer(data).run(9) == 1001

def test_backwards_compat():
    with open("e5.txt") as f:
        data = list(map(int, f.read().split(",")))
    assert Computer(data).run(5) == 7704130

# Day 7 tests
def test_feedbackless():
    amp = AmplificationCircuit(range(0,4+1), False)
    data = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    assert amp.calc_max_thruster(data) == (43210, (4,3,2,1,0))
    data = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
    assert amp.calc_max_thruster(data) == (54321, (0,1,2,3,4))
    data = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    assert amp.calc_max_thruster(data) == (65210, (1,0,4,3,2))
    
    with open("e7.txt") as f:
        data = list(map(int, f.read().split(",")))
    thrust, _ = amp.calc_max_thruster(data)
    assert thrust == 255840

def test_feedback():
    amp = AmplificationCircuit(range(5,9+1), True)
    data = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    assert amp.calc_max_thruster(data) == (139629729, (9,8,7,6,5))
    data = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
    assert amp.calc_max_thruster(data) == (18216, (9,7,8,5,6))

    with open("e7.txt") as f:
        data = list(map(int, f.read().split(",")))
    thrust, _ = amp.calc_max_thruster(data)
    assert thrust == 84088865