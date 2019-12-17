import intcode

x = 0
y = 0
scaffolding = set()
pos = (0, 0)


def output(o):
    global x, y, scaffolding, pos
    ch = chr(o)

    if ch == "^":
        pos = (x, y)

    if ch == ".":
        x += 1
    elif ch == "\n":
        y += 1
        x = 0
    else:
        scaffolding.add((x, y))
        x += 1

    print(ch, end="")


def is_intersection(coord):
    global scaffolding
    return ((coord[0], coord[1] + 1) in scaffolding) \
           and ((coord[0], coord[1] - 1) in scaffolding) \
           and ((coord[0] + 1, coord[1]) in scaffolding) \
           and ((coord[0] - 1, coord[1]) in scaffolding)


fp = open("17.txt")
data = list(map(lambda x: int(x), fp.read().split(",")))

intcode.execute_program(data, None, output)

intersections = list(filter(is_intersection, scaffolding))
print(sum(map(lambda coord: coord[0] * coord[1], intersections)))


def right(d):
    if d == (1, 0):
        return 0, 1
    if d == (0, 1):
        return -1, 0
    if d == (-1, 0):
        return 0, -1
    if d == (0, -1):
        return 1, 0


def left(d):
    if d == (1, 0):
        return 0, -1
    if d == (0, -1):
        return -1, 0
    if d == (-1, 0):
        return 0, 1
    if d == (0, 1):
        return 1, 0


path = ""
direction = (0, -1)
forward_count = 0
visited = set([pos])

while len(visited) < len(scaffolding):
    next_pos = (pos[0] + direction[0], pos[1] + direction[1])
    if next_pos in scaffolding:
        forward_count += 1
        pos = next_pos
        visited.add(pos)
    else:
        if forward_count > 0:
            path += str(forward_count)+","
        forward_count = 0
        l = left(direction)
        next_pos = (pos[0] + l[0], pos[1] + l[1])
        if next_pos in scaffolding:
            direction = l
            path += "L,"
        else:
            direction = right(direction)
            path += "R,"

path += str(forward_count)

print(path)

# got these by hand
a = "R,10,L,8,R,10,R,4"
b = "L,6,R,12,R,12,R,10"
c = "L,6,L,6,R,10"
program = "A,C,A,B,C,B,A,C,A,B\n"+a+"\n"+b+"\n"+c+"\nn\n"

i = 0
def get_input():
    global program, i
    ch = ord(program[i])
    i += 1
    return ch


def save_output(o):
    if o > 255:
        print(o)


data[0] = 2

intcode.execute_program(data, get_input, save_output)