from computer import Computer


class TileTypes:
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


class BreakOutAi:
    def __init__(self, computer):
        self.computer = computer
        self.computer.mem[0] = 2
        self.db = {}
        self._update_db(computer.run(0))

    def destroy_all_blocks(self):
        while self.get_positions(TileTypes.BLOCK):
            self.make_move()
        return self.db[-1, 0]  # score

    # Obviously inefficient, but simple :)
    def get_positions(self, tile_type):
        return [k for k, v in self.db.items() if v == tile_type]

    def make_move(self):
        self._update_db(self._make_move())
        return self.db

    def _update_db(self, it):
        try:
            while True:
                x = next(it)
                y = next(it)
                tile = next(it)
                self.db[x, y] = tile
        except StopIteration:
            pass

    def _make_move(self):
        ball_pos = self.get_positions(TileTypes.BALL)[0]
        pad_pos = self.get_positions(TileTypes.PADDLE)[0]
        if ball_pos[0] < pad_pos[0]:
            return self.computer.run(-1)
        elif ball_pos[0] > pad_pos[0]:
            return self.computer.run(1)
        else:
            return self.computer.run(0)


if __name__ == "__main__":
    with open("e13.txt") as f:
        data = list(map(int, f.read().split(",")))
    # 1
    print(len(BreakOutAi(Computer(data)).get_positions(TileTypes.BLOCK)))
    # 2
    print(BreakOutAi(Computer(data)).destroy_all_blocks())
