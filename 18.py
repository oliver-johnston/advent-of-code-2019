import string

keys = set("abcdefghijklmnopqrstuvwxyz")
doors = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


class Node:
    def __init__(self, x, y, letter):
        self.x = x
        self.y = y
        self.letter = letter

    def __repr__(self):
        return "({}, {}) = {}".format(self.x, self.y, self.letter)


class Path:
    def __init__(self, source, destination, distance, keys):
        self.source = source
        self.destination = destination
        self.distance = distance
        self.keys = keys

    def __repr__(self):
        return "{} -> {} = {} ({})".format(self.source, self.destination, self.distance, self.keys)


def get_nodes():
    fp = open("18.txt")
    data = fp.read()
    result = dict()
    x = 0
    y = 0
    for c in data:
        if c == '\n':
            y += 1
            x = 0
        else:
            if c != '#':
                result[(x, y)] = Node(x, y, c)
            x += 1
    return result


def get_paths_to_keys(source, cur_node, all_nodes, distance_so_far, keys_needed, visited):
    global keys, doors
    if (cur_node.x, cur_node.y) in visited:
        return []

    next_paths = []
    visited = set(list(visited) + [(cur_node.x, cur_node.y)])
    if cur_node.letter in keys and cur_node.letter != source:
        next_paths = next_paths + [Path(source, cur_node.letter, distance_so_far, keys_needed)]

    if cur_node.letter in doors:
        keys_needed = set(list(keys_needed) + [chr(ord(cur_node.letter) + 32)])

    if cur_node.letter in keys:
        keys_needed = set(list(keys_needed) + [cur_node.letter])

    points = [(cur_node.x + 1, cur_node.y),
              (cur_node.x - 1, cur_node.y),
              (cur_node.x, cur_node.y + 1),
              (cur_node.x, cur_node.y - 1)]
    next_nodes = [all_nodes[coord] for coord in points if coord in all_nodes]
    for n in next_nodes:
        next_paths = next_paths + get_paths_to_keys(source,
                                                    n,
                                                    all_nodes,
                                                    distance_so_far + 1,
                                                    keys_needed,
                                                    visited)
    return next_paths


nodes = get_nodes()
key_nodes = list(filter(lambda node: node.letter in keys or node.letter == '@', nodes.values()))

print("Calculating paths for {} nodes, {} keys".format(len(nodes), len(key_nodes)))

paths = []
for n in key_nodes:
    paths = paths + get_paths_to_keys(n.letter, n, nodes, 0, set(), set())

print("Calculated {} paths".format(len(paths)))

routes = dict()
routes["@"] = 0
queue = ['@']
while len(queue) > 0:
    cur = queue.pop(0)
    distance_so_far = routes[cur]

    cur_key = cur[0]
    to_visit = [p for p in paths if p.source == cur_key
                and p.destination not in cur
                and all(map(lambda k: k in cur, p.keys))]
    for x in to_visit:
        next = x.destination + "".join(sorted(cur))
        if next not in routes:
            queue.append(next)
        routes[next] = min(routes.get(next, 99999999), distance_so_far + x.distance)

print(min([routes[r] for r in routes if len(r) == len(key_nodes)]))
