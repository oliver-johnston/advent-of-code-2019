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


class Frontier:
    def __init__(self, node, keys):
        self.keys = keys
        self.node = node

    def __repr__(self):
        return "{} ({})".format(self.node, self.keys)


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


def discover_paths(node, all_nodes):
    global keys, doors
    frontiers = [Frontier(node, [])]
    paths = []
    distance = 0
    visited = set()
    while len(frontiers) > 0:
        next_frontiers = []
        for f in frontiers:
            if (f.node.x, f.node.y) in visited:
                continue

            visited.add((f.node.x, f.node.y))

            keys_needed = f.keys
            if f.node.letter in keys and f.node != node:
                paths.append(Path(node.letter, f.node.letter, distance, keys_needed))
                keys_needed = keys_needed + [f.node.letter]
            elif f.node.letter in doors:
                keys_needed = keys_needed + [chr(ord(f.node.letter) + 32)]

            points = [(f.node.x + 1, f.node.y),
                      (f.node.x - 1, f.node.y),
                      (f.node.x, f.node.y + 1),
                      (f.node.x, f.node.y - 1)]
            next_nodes = [all_nodes[coord] for coord in points if coord in all_nodes]
            next_frontiers = next_frontiers + [Frontier(n, keys_needed) for n in next_nodes]
        frontiers = next_frontiers
        distance += 1
    return paths


nodes = get_nodes()
key_nodes = list(filter(lambda node: node.letter in keys or node.letter == '@', nodes.values()))

print("Calculating paths for {} nodes, {} keys".format(len(nodes), len(key_nodes)))

starts = [n for n in nodes.values() if n.letter == '@']
subsets = [discover_paths(s, nodes) for s in starts]

droid_paths = []
for s in subsets:
    keys_in_subset = [p.destination for p in s]
    nodes_in_subset = [n for n in nodes.values() if n.letter in keys_in_subset]
    for n in nodes_in_subset:
        s = s + discover_paths(n, nodes)
    droid_paths.append(s)

start = "|".join(["@" for _ in droid_paths])
routes = dict()
routes[start] = 0
queue = [start]
while len(queue) > 0:
    cur = queue.pop(0)
    distance_so_far = routes[cur]
    droid_routes = cur.split("|")

    for droid_num in range(0, len(droid_routes)):
        cur_droid_route = droid_routes[droid_num]
        paths = droid_paths[droid_num]
        cur_key = cur_droid_route[0]
        to_visit = [p for p in paths if p.source == cur_key
                    and p.destination not in cur
                    and all(map(lambda k: k in cur, p.keys))]
        for x in to_visit:
            next_droid = x.destination + "".join(sorted(cur_droid_route))
            next_droids = []
            for i in range(0, len(droid_routes)):
                if i == droid_num:
                    next_droids.append(next_droid)
                else:
                    next_droids.append(droid_routes[i])
            next = "|".join(next_droids)
            if next not in routes:
                queue.append(next)
            routes[next] = min(routes.get(next, 99999999), distance_so_far + x.distance)

max_len = max([len(r1) for r1 in routes])
print(min([routes[r] for r in routes if len(r) == max_len]))
