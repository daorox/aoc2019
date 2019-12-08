from copy import deepcopy
from itertools import permutations


class Computer:
    def __init__(self, mem, ip=0):
        self.mem = deepcopy(mem)
        self.ip = ip
        self.input_value = None

    def add(self):
        self.mem[self.param_idx(2,True)] =self.param_value(0) + self.param_value(1)
        self.ip += 4

    def mul(self):
        self.mem[self.param_idx(2,True)] = self.param_value(0)  *self.param_value(1)
        self.ip += 4

    def input(self):
        self.mem[self.param_idx(0,True)] = self.input_value
        self.input_value = None
        self.ip += 2

    def output(self):
        out = self.param_value(0)
        self.ip += 2
        return out

    def je(self):
        self.ip = self.param_value(1) if self.param_value(0) else self.ip + 3
    
    def jne (self):
        self.ip = self.param_value(1) if not self.param_value(0) else self.ip + 3

    def lt(self):
        self.mem[self.param_idx(2,True)] = 1 if self.param_value(0) < self.param_value(1) else 0
        self.ip += 4
    
    def eq(self):
        self.mem[self.param_idx(2,True)] = 1 if self.param_value(0) == self.param_value(1) else 0
        self.ip += 4

    # TODO: clean up this mess
    def param_idx(self, idx, assign=False):
        s = str(self.mem[self.ip])

        if len(s) == 1:
            return self.mem[self.ip+idx+1]
        op, remaining = s[-2:], s[:-2]


        if len(remaining) == 0:
            return int(op)

        if len(remaining) == 1:
            conf = (int(remaining[-1]), 0, 0)
        if len(remaining) == 2:
            conf = (int(remaining[-1]), int(remaining[-2]), 0)
        if len(remaining) == 3:
            conf = (int(remaining[-1]), int(remaining[-2]), int(remaining[-3]))
        
        if conf[idx] == 0 or assign:
            return self.mem[self.ip+idx+1]
        else:
            return self.ip+idx+1

    def param_value(self, idx):
        return self.mem[self.param_idx(idx)]
    
    def op(self):
        s = str(self.mem[self.ip])
        return int(s[-2:])
        

    def run(self, input_value):
        self.input_value = input_value
        opcode = self.mem[self.ip]

        # assume first instruction is 3
        if opcode == 3:
            self.input()
        
        while opcode != 99:
            opcode = self.op()
            if opcode == 1: self.add()
            if opcode == 2: self.mul()
            if opcode == 3:
                if self.input_value:
                    self.input()
                else:
                    return
            if opcode == 4: 
                return self.output()
            if opcode == 5: self.je()
            if opcode == 6: self.jne()
            if opcode == 7: self.lt()
            if opcode == 8: self.eq()

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
            self.computers[i].run(phase)
    
    def _apply_input(self, inp):
        while inp != None:
            for computer in self.computers:
                output = computer.run(inp)
                if output:
                    inp = output
                else:
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
    with open("e7.txt") as f:
        data = list(map(int, f.read().split(",")))
    # 1
    amp = AmplificationCircuit(range(0,4+1), False)
    print(amp.calc_max_thruster(data, 0))
    # 2
    amp = AmplificationCircuit(range(5,9+1), True)
    print(amp.calc_max_thruster(data, 0))
