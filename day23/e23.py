from computer import Computer


class Network:
    NAT_ADDRESS = 255

    def __init__(self, data, computer_count=50):
        self.data = data
        self.init_network()
        self.message_queues = {i: [] for i in range(computer_count)}
        self.nat = []
        self.nat_ys = set()
        self.first_nat_y = None

    def init_network(self, computer_count=50):
        self.computers = [Computer(self.data) for _ in range(computer_count)]
        for i, c in enumerate(self.computers):
            for _ in c.run([i]):
                pass

    def all_idles(self):
        return all(len(q) is 0 for q in self.message_queues.values())

    def send_messages(self, it):
        while True:
            try:
                dest = next(it)
                x = next(it)
                y = next(it)
                if dest == Network.NAT_ADDRESS:
                    if self.first_nat_y is None:
                        self.first_nat_y = y
                    self.nat = [x, y]
                else:
                    self.message_queues[dest].append([x, y])
            except StopIteration:
                break

    def get_msg(self, computer_addr):
        msg = [-1]
        if self.message_queues[computer_addr]:
            msg = self.message_queues[computer_addr].pop(0)
        return msg

    def process_computer_queues(self):
        idle_count = 0
        while True:
            for i, c in enumerate(self.computers):
                it = c.run(self.get_msg(i))
                self.send_messages(it)

            if self.all_idles():
                idle_count += 1
            if idle_count > 3:
                x, y = self.nat
                self.message_queues[0].append([x, y])
                if y in self.nat_ys:
                    return y

                self.nat_ys.add(y)
                idle_count = 0


if __name__ == "__main__":
    with open("e23.txt") as f:
        data = list(map(int, f.read().split(",")))

    n = Network(data)
    # 2
    print(n.process_computer_queues())
    # 1
    print(n.first_nat_y)
