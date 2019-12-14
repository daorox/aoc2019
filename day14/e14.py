from collections import defaultdict
import math
import re

ORE = "ORE"
FUEL = "FUEL"


def parse_item(s):
    amount, material = s.split()
    return (int(amount), material)


# Convert data to format {material: (amount_produced, [prerequisites])}
def parse_data(data):
    reqs = {}
    for line in data.splitlines(False):
        line = re.findall(r"(\d+ \w+)", line)
        amount, prod = parse_item(line[-1])
        reqs[prod] = (amount, [parse_item(req) for req in line[:-1]])
    return reqs


class Stoichiometry:
    def __init__(self, reqs):
        self.reqs = reqs
        self._set_levels()
        self.wallet = defaultdict(int)

    def get_ore_usage(self, fuel_req):
        required = [(fuel_req, FUEL)]

        self.wallet = defaultdict(int)
        ore = 0
        while required:
            amount_required, material = required.pop()

            if material == ORE:
                ore += amount_required
                break
            amount_required = self._use_wallet(material, amount_required)

            if amount_required > 0:
                required.extend(self._produce_material(material, amount_required))
            required = self._group_reqs(required)
            required = sorted(required, key=lambda x: self.levels[x[1]])
        return ore

    def get_max_fuel(self, ore_available):
        min_fuel = 0
        max_fuel = ore_available
        while max_fuel >= min_fuel:
            cur_fuel = (max_fuel + min_fuel) // 2
            ore_required = self.get_ore_usage(cur_fuel)
            if ore_required > ore_available:
                max_fuel = cur_fuel - 1
            elif ore_required < ore_available:
                if self.get_ore_usage(cur_fuel + 1) > ore_available:
                    return cur_fuel
                min_fuel = cur_fuel + 1
            else:
                return cur_fuel

    def _group_reqs(self, reqs):
        db = defaultdict(int)
        for r in reqs:
            am, material = r
            db[material] += am
        return [(a, n) for n, a in db.items()]

    def _dist_to_ore(self, s, cur=0):
        if s == ORE:
            return cur
        _, r = self.reqs[s]
        return max(self._dist_to_ore(r2, cur + 1) for _, r2 in r)

    def _set_levels(self):
        self.levels = {item: self._dist_to_ore(item) for item in self.reqs.keys()}
        self.levels[ORE] = 0

    def _scale_requirements(self, new_reqs, factor):
        res = []
        for item in new_reqs:
            a, b = item
            res.append((a * factor, b))
        return res

    def _use_wallet(self, material, amount):
        if self.wallet[material] >= amount:
            self.wallet[material] -= amount
            amount = 0
        else:
            amount -= self.wallet[material]
            self.wallet[material] = 0
        return amount

    def _produce_material(self, material, amount):
        produced_amount, new_reqs = self.reqs[material]
        times_produced = int(math.ceil(amount / produced_amount))
        produced_amount *= times_produced
        new_reqs = self._scale_requirements(new_reqs, times_produced)
        self.wallet[material] += produced_amount - (amount // produced_amount) * amount
        return new_reqs


if __name__ == "__main__":

    with open("e14.txt") as f:
        data = f.read()
    reqs = parse_data(data)
    sto = Stoichiometry(reqs)
    # 1
    print(sto.get_ore_usage(1))
    # 2
    print(sto.get_max_fuel(1000000000000))

