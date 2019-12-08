from e6 import Orbits, get_mappings

basic_data_orbits = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""

basic_data_transfers = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""


def test_count_orbits():
    solver = Orbits(*get_mappings(basic_data_orbits.splitlines()))
    assert solver.count_orbits() == 42

    with open("e6.txt") as f:
        data = list(x.rstrip() for x in f.readlines())
    solver = Orbits(*get_mappings(data))
    assert solver.count_orbits() == 204521


def test_count_orbital_transfers():
    solver = Orbits(*get_mappings(basic_data_transfers.splitlines()))
    assert solver.count_orbital_transfers("E", "L") == 1
    assert solver.count_orbital_transfers("L", "E") == 1
    assert solver.count_orbital_transfers("YOU", "SAN") == 4

    with open("e6.txt") as f:
        data = list(x[:-1] for x in f.readlines())
    solver = Orbits(*get_mappings(data))
    assert solver.count_orbital_transfers("YOU", "SAN") == 307
