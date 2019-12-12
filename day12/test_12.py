from e12 import MoonSimulator, parse_data

data1 = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""

data2 = """<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""


def test_tot_energy():
    with open("e12.txt") as f:
        data_real = f.read()
    assert MoonSimulator(parse_data(data1)).tot_energy(10) == 179
    assert MoonSimulator(parse_data(data2)).tot_energy(100) == 1940
    assert MoonSimulator(parse_data(data_real)).tot_energy(1000) == 5937


def test_steps_until_repeating_universe():
    with open("e12.txt") as f:
        data_real = f.read()
    assert MoonSimulator(parse_data(data1)).steps_until_repeating_universe() == 2772
    assert (
        MoonSimulator(parse_data(data_real)).steps_until_repeating_universe()
        == 376203951569712
    )
