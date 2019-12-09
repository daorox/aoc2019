from copy import deepcopy
from itertools import permutations
from collections import defaultdict


class Computer:
    def __init__(self, mem, ip=0):
        self.mem = deepcopy(mem)
        self.ip = ip
        self.input_value = None
        self.rel_base = 0
        self.extra_mem = defaultdict(int)

    def store_mem(self, idx, val):
        idx = self.param_idx(idx, True)
        if idx < len(self.mem):
            self.mem[idx] = val
        else:
            self.extra_mem[idx] = val

    def get_mem(self, idx):
        idx = self.param_idx(idx)
        if idx < len(self.mem):
            return self.mem[idx]
        else:
            return self.extra_mem[idx]

    def add(self):
        self.store_mem(2, self.get_mem(0) + self.get_mem(1))
        self.ip += 4

    def mul(self):
        self.store_mem(2, self.get_mem(0) * self.get_mem(1))
        self.ip += 4

    def input(self):
        self.store_mem(0, self.input_value)
        self.input_value = None
        self.ip += 2

    def output(self):
        out = self.get_mem(0)
        self.ip += 2
        return out

    def je(self):
        self.ip = self.get_mem(1) if self.get_mem(0) else self.ip + 3

    def jne(self):
        self.ip = self.get_mem(1) if not self.get_mem(0) else self.ip + 3

    def lt(self):
        self.store_mem(2, 1 if self.get_mem(0) < self.get_mem(1) else 0)
        self.ip += 4

    def eq(self):
        b = 1 if self.get_mem(0) == self.get_mem(1) else 0
        self.store_mem(2, b)
        self.ip += 4

    def relative_base(self):
        self.rel_base += self.get_mem(0)
        self.ip += 2

    # TODO: clean up this mess
    def param_idx(self, idx, assign=False):
        s = str(self.mem[self.ip])

        if len(s) == 1:
            return self.mem[self.ip + idx + 1]
        op, remaining = s[-2:], s[:-2]

        if len(remaining) == 0:
            return int(op)

        if len(remaining) == 1:
            conf = (int(remaining[-1]), 0, 0)
        if len(remaining) == 2:
            conf = (int(remaining[-1]), int(remaining[-2]), 0)
        if len(remaining) == 3:
            conf = (int(remaining[-1]), int(remaining[-2]), int(remaining[-3]))
        if conf[idx] == 2:
            return self.mem[self.ip + idx + 1] + self.rel_base
        elif conf[idx] == 0 or assign:
            return self.mem[self.ip + idx + 1]
        elif conf[idx] == 1:
            return self.ip + idx + 1
        else:
            print("Unimplemented mode")

    def get_idx(self, idx, assign, mode):
        if mode == 2:
            return self.mem[self.ip + idx + 1] + self.rel_base
        elif mode == 0 or assign:
            return self.mem[self.ip + idx + 1]
        elif mode == 1:
            return self.ip + idx + 1

    def op(self):
        s = str(
            self.mem[self.ip] if self.ip < len(self.mem) else self.extra_mem[self.ip]
        )
        return int(s[-2:])

    def run(self, input_value):
        self.input_value = input_value

        opcode = self.op()

        while opcode != 99:
            opcode = self.op()
            if opcode == 1:
                self.add()
            if opcode == 2:
                self.mul()
            if opcode == 3:
                if self.input_value is not None:
                    self.input()
                else:
                    return
            if opcode == 4:
                yield self.output()
            if opcode == 5:
                self.je()
            if opcode == 6:
                self.jne()
            if opcode == 7:
                self.lt()
            if opcode == 8:
                self.eq()
            if opcode == 9:
                self.relative_base()


class AmplificationCircuit:
    def __init__(self, phase_range, use_feedback_loop):
        self.phase_range = list(phase_range)
        self.use_feedback_loop = use_feedback_loop

    def calc_max_thruster(self, data, start_input=0):
        self._reset_progress()
        for phases in permutations(self.phase_range):
            self.computers = [Computer(data) for _ in range(len(phases))]
            self._apply_amplifiers(phases)
            output = self._apply_input(start_input)
            self._store_progress(output, phases)
        return self._get_progress()

    def _apply_amplifiers(self, phases):
        for i, phase in enumerate(phases):
            try:
                next(self.computers[i].run(phase))
            except StopIteration:
                pass

    def _apply_input(self, inp):
        while True:
            for computer in self.computers:
                try:
                    inp = next(computer.run(inp))
                except StopIteration:
                    return inp
            if not self.use_feedback_loop:
                return inp

    def _reset_progress(self):
        self.max_thrust = 0
        self.best_phase = ()

    def _store_progress(self, output, phase):
        if output > self.max_thrust:
            self.max_thrust = output
            self.best_phase = phase

    def _get_progress(self):
        return (self.max_thrust, self.best_phase)


if __name__ == "__main__":
    with open("e9.txt") as f:
        data = list(map(int, f.read().split(",")))
    # 1
    for v in Computer(data).run(1):
        print(v)
    # 2
    for v in Computer(data).run(2):
        print(v)

