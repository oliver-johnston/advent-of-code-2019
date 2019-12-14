class Position:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def add(self, x, y, z):
        self.x += x
        self.y += y
        self.z += z


class Moon:
    def __init__(self, x, y, z):
        self.position = Position(x, y, z)
        self.velocity = Position(0, 0, 0)

    def apply_gravity(self, other):
        dx = other.position.x - self.position.x
        dy = other.position.y - self.position.y
        dz = other.position.z - self.position.z

        dx = max(min(dx, 1), -1)
        dy = max(min(dy, 1), -1)
        dz = max(min(dz, 1), -1)

        self.velocity.add(dx, dy, dz)

    def apply_velocity(self):
        self.position.add(self.velocity.x, self.velocity.y, self.velocity.z)

    def get_energy(self):
        pot = abs(self.position.x) + abs(self.position.y) + abs(self.position.z)
        kin = abs(self.velocity.x) + abs(self.velocity.y) + abs(self.velocity.z)
        return pot * kin


def step(moons):
    for a in moons:
        for b in moons:
            a.apply_gravity(b)

    for m in moons:
        m.apply_velocity()


moons = [
    Moon(13, 9, 5),
    Moon(8, 14, -2),
    Moon(-5, 4, 11),
    Moon(2, -6, 1)
]

for i in range(0, 1000):
    step(moons)

print(sum(m.get_energy() for m in moons))

moons = [
    Moon(13, 9, 5),
    Moon(8, 14, -2),
    Moon(-5, 4, 11),
    Moon(2, -6, 1)
]

energies = set([sum(m.get_energy() for m in moons)])
while True:
    step(moons)
    energy = sum(m.get_energy() for m in moons)
    print(len(energies))
    if energy in energies:
        break
    energies.add(energy)
