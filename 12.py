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


def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    return a * b / gcd(a, b)


def get_moons():
    return [
        Moon(13, 9, 5),
        Moon(8, 14, -2),
        Moon(-5, 4, 11),
        Moon(2, -6, 1)
    ]


def x_equal(a, b):
    return a.position.x == b.position.x and a.velocity.x == b.velocity.x


def y_equal(a, b):
    return a.position.y == b.position.y and a.velocity.y == b.velocity.y


def z_equal(a, b):
    return a.position.z == b.position.z and a.velocity.z == b.velocity.z


moons = get_moons()

for i in range(0, 1000):
    step(moons)

print(sum(m.get_energy() for m in moons))

initial_moons = get_moons()
moons = get_moons()

x_loop = 0
y_loop = 0
z_loop = 0

step_num = 0
while x_loop == 0 or y_loop == 0 or z_loop == 0:
    step(moons)
    step_num += 1

    if x_loop == 0 and all(map(lambda i: x_equal(moons[i], initial_moons[i]), range(0, len(moons)))):
        x_loop = step_num

    if y_loop == 0 and all(map(lambda i: y_equal(moons[i], initial_moons[i]), range(0, len(moons)))):
        y_loop = step_num

    if z_loop == 0 and all(map(lambda i: z_equal(moons[i], initial_moons[i]), range(0, len(moons)))):
        z_loop = step_num

print(lcm(x_loop, lcm(y_loop, z_loop)))
