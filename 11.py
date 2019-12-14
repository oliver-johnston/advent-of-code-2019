import intcode


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def equals(self, other):
        return self.x == other.x and self.y == other.y


class Panel:
    def __init__(self, point):
        self.point = point
        self.color = -1


class Painter:
    def __init__(self, start_colour):
        self.location = Point(0, 0)
        self.direction = 0
        self.output_type = 0
        start_panel = Panel(self.location)
        start_panel.color = start_colour
        self.panels = [start_panel]

    def get_current_panel(self):
        p = next((p for p in self.panels if p.point.equals(self.location)), None)
        if p is None:
            p = Panel(self.location)
            self.panels.append(p)
        return p

    def get_panel(self, point):
        return next((p for p in self.panels if p.point.equals(point)), None)

    def get_current_panel_color(self):
        panel = self.get_current_panel()
        if panel.color == -1:
            return 0
        return panel.color

    def output(self, o):
        if self.output_type == 0:
            self.paint(o)
        else:
            self.change_direction(o)

        self.output_type = (self.output_type + 1) % 2

    def change_direction(self, o):
        if o == 0:
            self.direction = (self.direction - 1) % 4
        else:
            self.direction = (self.direction + 1) % 4

        self.move_forward()

    def move_forward(self):
        dx = 0
        dy = 0
        if self.direction == 0:
            dy = -1
        elif self.direction == 1:
            dx = 1
        elif self.direction == 2:
            dy = 1
        else:
            dx = -1
        self.location = Point(self.location.x + dx, self.location.y + dy)

    def paint(self, color):
        self.get_current_panel().color = color

    def run(self, program):
        intcode.execute_program(program, self.get_current_panel_color, self.output)


program = [3, 8, 1005, 8, 290, 1106, 0, 11, 0, 0, 0, 104, 1, 104, 0, 3, 8, 1002, 8, -1, 10, 1001, 10, 1, 10, 4, 10, 108,
           1, 8, 10, 4, 10, 1002, 8, 1, 28, 1006, 0, 59, 3, 8, 1002, 8, -1, 10, 101, 1, 10, 10, 4, 10, 108, 0, 8, 10, 4,
           10, 101, 0, 8, 53, 3, 8, 1002, 8, -1, 10, 101, 1, 10, 10, 4, 10, 1008, 8, 0, 10, 4, 10, 101, 0, 8, 76, 1006,
           0, 81, 1, 1005, 2, 10, 3, 8, 102, -1, 8, 10, 1001, 10, 1, 10, 4, 10, 1008, 8, 1, 10, 4, 10, 1002, 8, 1, 105,
           3, 8, 102, -1, 8, 10, 1001, 10, 1, 10, 4, 10, 108, 1, 8, 10, 4, 10, 1001, 8, 0, 126, 3, 8, 1002, 8, -1, 10,
           1001, 10, 1, 10, 4, 10, 108, 1, 8, 10, 4, 10, 1002, 8, 1, 148, 3, 8, 102, -1, 8, 10, 101, 1, 10, 10, 4, 10,
           1008, 8, 1, 10, 4, 10, 1001, 8, 0, 171, 3, 8, 1002, 8, -1, 10, 1001, 10, 1, 10, 4, 10, 1008, 8, 0, 10, 4, 10,
           101, 0, 8, 193, 1, 1008, 8, 10, 1, 106, 3, 10, 1006, 0, 18, 3, 8, 1002, 8, -1, 10, 1001, 10, 1, 10, 4, 10,
           108, 0, 8, 10, 4, 10, 1001, 8, 0, 225, 1, 1009, 9, 10, 1006, 0, 92, 3, 8, 1002, 8, -1, 10, 1001, 10, 1, 10,
           4, 10, 108, 0, 8, 10, 4, 10, 1001, 8, 0, 254, 2, 1001, 8, 10, 1, 106, 11, 10, 2, 102, 13, 10, 1006, 0, 78,
           101, 1, 9, 9, 1007, 9, 987, 10, 1005, 10, 15, 99, 109, 612, 104, 0, 104, 1, 21102, 1, 825594852136, 1, 21101,
           0, 307, 0, 1106, 0, 411, 21101, 0, 825326580628, 1, 21101, 0, 318, 0, 1105, 1, 411, 3, 10, 104, 0, 104, 1, 3,
           10, 104, 0, 104, 0, 3, 10, 104, 0, 104, 1, 3, 10, 104, 0, 104, 1, 3, 10, 104, 0, 104, 0, 3, 10, 104, 0, 104,
           1, 21102, 179557207043, 1, 1, 21101, 0, 365, 0, 1106, 0, 411, 21101, 0, 46213012483, 1, 21102, 376, 1, 0,
           1106, 0, 411, 3, 10, 104, 0, 104, 0, 3, 10, 104, 0, 104, 0, 21101, 988648727316, 0, 1, 21102, 399, 1, 0,
           1105, 1, 411, 21102, 988224959252, 1, 1, 21101, 0, 410, 0, 1106, 0, 411, 99, 109, 2, 21201, -1, 0, 1, 21101,
           0, 40, 2, 21102, 1, 442, 3, 21101, 432, 0, 0, 1105, 1, 475, 109, -2, 2105, 1, 0, 0, 1, 0, 0, 1, 109, 2, 3,
           10, 204, -1, 1001, 437, 438, 453, 4, 0, 1001, 437, 1, 437, 108, 4, 437, 10, 1006, 10, 469, 1102, 0, 1, 437,
           109, -2, 2105, 1, 0, 0, 109, 4, 2102, 1, -1, 474, 1207, -3, 0, 10, 1006, 10, 492, 21101, 0, 0, -3, 21202, -3,
           1, 1, 22102, 1, -2, 2, 21101, 0, 1, 3, 21102, 511, 1, 0, 1105, 1, 516, 109, -4, 2105, 1, 0, 109, 5, 1207, -3,
           1, 10, 1006, 10, 539, 2207, -4, -2, 10, 1006, 10, 539, 21201, -4, 0, -4, 1106, 0, 607, 21202, -4, 1, 1,
           21201, -3, -1, 2, 21202, -2, 2, 3, 21101, 558, 0, 0, 1106, 0, 516, 22101, 0, 1, -4, 21101, 1, 0, -1, 2207,
           -4, -2, 10, 1006, 10, 577, 21102, 1, 0, -1, 22202, -2, -1, -2, 2107, 0, -3, 10, 1006, 10, 599, 21201, -1, 0,
           1, 21101, 0, 599, 0, 105, 1, 474, 21202, -2, -1, -2, 22201, -4, -2, -4, 109, -5, 2106, 0, 0]

#painter = Painter(-1)
#painter.run(program)

#print(sum(1 for p in painter.panels if p.color != -1))


painter = Painter(1)
painter.run(program)

max_x = max(map(lambda p: p.point.x, painter.panels))
min_x = min(map(lambda p: p.point.x, painter.panels))
max_y = max(map(lambda p: p.point.y, painter.panels))
min_y = min(map(lambda p: p.point.y, painter.panels))

for j in range(min_y, max_y+1):
    for i in range(min_x, max_x+1):
        panel = painter.get_panel(Point(i, j))
        if panel is not None and panel.color == 1:
            print("#", end="")
        else:
            print(" ", end="")
    print("")
