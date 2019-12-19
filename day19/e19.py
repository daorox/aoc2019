from computer import Computer


class BeamAnalyzer:
    def __init__(self, computer_input):
        self.computer_input = computer_input

    def count_beam_points(self, square_size):
        return sum(
            p
            for x in range(square_size)
            for y in range(square_size)
            for p in Computer(self.computer_input).run([x, y])
        )

    def estimate_slope(self):
        for y in range(1, 150):
            x = self.find_rightmost_beam(y)
            print(f"x/y={x}/{y}={x/y}")

    def find_square(self, size):
        # Subtract one to account for the current row/col
        size = size - 1
        y = size
        while True:
            x_right = self.find_rightmost_beam(y)

            if self.is_square(x_right, y, size):
                return x_right - size, y
            y += 1

    def pos_has_beam(self, x, y):
        return next(Computer(self.computer_input).run([x, y]))

    def find_rightmost_beam(self, y):
        in_beam = False
        # Seems to be rougly the slope for the rightmost pixel
        x = y * 2
        while True:
            if self.pos_has_beam(x, y):
                in_beam = True
            elif in_beam:
                # Just left beam
                return x - 1
            x += 1

    def is_square(self, x_right, y_up, size):
        x_left = x_right - size
        y_down = y_up + size

        return (
            self.pos_has_beam(x_left, y_up)
            and self.pos_has_beam(x_right, y_up)
            and self.pos_has_beam(x_left, y_down)
            and self.pos_has_beam(x_right, y_down)
        )

    def print_map(self, bbox):
        y_min, x_min, y_max, x_max = bbox

        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                v = next(Computer(self.computer_input).run([x, y]))
                print(v if v else ".", end="")
            print()


if __name__ == "__main__":
    with open("e19.txt") as f:
        data = list(map(int, f.read().split(",")))

    print(BeamAnalyzer(data).count_beam_points(50))
    print(BeamAnalyzer(data).find_square(100))
