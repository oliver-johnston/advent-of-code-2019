class Node:
    def __init__(self, x, y, letter, is_outer):
        self.x = x
        self.y = y
        self.letter = letter
        self.is_outer = is_outer
        self.is_inner = not is_outer
        self.neighbours = None

    def __repr__(self):
        return "({}, {}) = {}{}".format(self.x, self.y, self.letter, " outer" if self.is_outer else "")

    def get_neighbours(self, nodes):
        if self.neighbours is not None:
            return self.neighbours
        self.neighbours = [n for n in nodes if self.is_neighbour(n)]
        return self.neighbours

    def is_neighbour(self, other):
        if self.x == other.x and self.y == other.y:
            return False

        x_diff = abs(self.x - other.x)
        y_diff = abs(self.y - other.y)

        if (x_diff + y_diff) == 1:
            return True

        if self.letter == ".":
            return False

        return self.letter == other.letter


def get_nodes():
    fp = open("20.txt")
    data = fp.read()
    result = dict()
    rows = [list(r) for r in data.split("\n")]
    for x in range(0, len(rows)):
        row = rows[x]
        for y in range(0, len(row)):
            c = row[y]
            if c == ".":
                if (x, y) not in result:
                    result[(x, y)] = Node(x, y, c, False)
            elif c not in ("#", " "):
                code = c
                adjacent = [p for p in [(x + 1, y), (x, y + 1)]
                            if 0 <= p[0] < len(rows) and 0 <= p[1] < len(row)]
                other_code_p = [p for p in adjacent if rows[p[0]][p[1]] not in ("#", ".", " ")][0]
                code += rows[other_code_p[0]][other_code_p[1]]
                rows[other_code_p[0]][other_code_p[1]] = " "
                diff = (other_code_p[0] - x, other_code_p[1] - y)
                point_options = [p for p in [(other_code_p[0] + diff[0], other_code_p[1] + diff[1]),
                                             (x - diff[0], y - diff[1])]
                                 if 0 <= p[0] < len(rows) and 0 <= p[1] < len(row)]
                teleport_p = [p for p in point_options if rows[p[0]][p[1]] == "."][0]
                is_outer = x == 0 or x == 1 or y == 0 or y == 1 or \
                           x == len(rows) - 1 or x == len(rows) - 2 or \
                           y == len(row) - 1 or y == len(row) - 2
                result[teleport_p] = Node(teleport_p[0], teleport_p[1], code, is_outer)

    return result


nodes = get_nodes().values()

queue = [(n, 0) for n in nodes if n.letter == "AA"]
visited = set([(n.x, n.y, 0) for n in nodes if n.letter == "AA"])
steps = 0
while len(queue) > 0:
    next_queue = []
    while len(queue) > 0:
        cur = queue.pop(0)

        node = cur[0]
        level = cur[1]

        if level >= 30:
            continue

        visited.add((node.x, node.y, level))
        if node.letter == "ZZ" and level == 0:
            print("ZZ found after {} steps".format(steps))
            exit()
        neighbours = node.get_neighbours(nodes)
        for n in neighbours:
            n_level = level
            if node.letter != "." and n.letter != ".":
                n_level += -1 if node.is_outer else 1

            if n_level >= 0 and (n.x, n.y, n_level) not in visited:
                next_queue.append((n, n_level))

    steps += 1
    queue = next_queue

    if steps % 50 == 0:
        print("Steps so far: {}. Queue size: {}".format(steps, len(queue)))


