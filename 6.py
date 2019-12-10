class Orbit:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.depth = parent.depth + 1 if parent is not None else 0


def build_orbits_tree(data):
    orbits = dict(COM=Orbit("COM", None))

    for line in data:
        split = line.split(")")
        parent = split[0]
        child = split[1]
        if parent not in orbits:
            data.append(line)
        else:
            orbits[child] = Orbit(child, orbits[parent])

    return orbits


def count_orbits(orbit):
    if orbit.parent is None:
        return 0
    else:
        return 1 + count_orbits(orbit.parent)


def count_transfers(src, dest):
    if src == dest:
        return 0

    if src.depth > dest.depth:
        return 1 + count_transfers(src.parent, dest)
    else:
        return 1 + count_transfers(src, dest.parent)


fp = open("6.txt")
data = fp.read().splitlines()
orbits = build_orbits_tree(data)
print(sum(count_orbits(o) for o in orbits.values()))
print(count_transfers(orbits["YOU"].parent, orbits["SAN"].parent))