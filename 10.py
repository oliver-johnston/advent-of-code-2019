import math
import itertools


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def parse_points(asteroid_string):
    asteroids = []
    lines = asteroid_string.splitlines()
    for i in range(0, len(lines)):
        chars = lines[i]
        for j in range(0, len(chars)):
            if chars[j] == '#':
                asteroids.append(Point(j, i))
    return asteroids


def angle(a, b):
    degrees = math.degrees(math.atan2(b.x - a.x, a.y - b.y))
    if degrees >= 0:
        return degrees
    return degrees + 360


def distance(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


asteroid_string = """.#......#...#.....#..#......#..##..#
..#.......#..........#..##.##.......
##......#.#..#..#..##...#.##.###....
..#........#...........#.......##...
.##.....#.......#........#..#.#.....
.#...#...#.....#.##.......#...#....#
#...#..##....#....#......#..........
....#......#.#.....#..#...#......#..
......###.......#..........#.##.#...
#......#..#.....#..#......#..#..####
.##...##......##..#####.......##....
.....#...#.........#........#....#..
....##.....#...#........#.##..#....#
....#........#.###.#........#...#..#
....#..#.#.##....#.........#.....#.#
##....###....##..#..#........#......
.....#.#.........#.......#....#....#
.###.....#....#.#......#...##.##....
...##...##....##.........#...#......
.....#....##....#..#.#.#...##.#...#.
#...#.#.#.#..##.#...#..#..#..#......
......#...#...#.#.....#.#.....#.####
..........#..................#.#.##.
....#....#....#...#..#....#.....#...
.#####..####........#...............
#....#.#..#..#....##......#...#.....
...####....#..#......#.#...##.....#.
..##....#.###.##.#.##.#.....#......#
....#.####...#......###.....##......
.#.....#....#......#..#..#.#..#.....
..#.......#...#........#.##...#.....
#.....####.#..........#.#.......#...
..##..#..#.....#.#.........#..#.#.##
.........#..........##.#.##.......##
#..#.....#....#....#.#.......####..#
..............#.#...........##.#.#.."""

asteroids = parse_points(asteroid_string)

best_count = 0
best_asteroid = None

for a in asteroids:
    count = len(set(map(lambda b: angle(a, b), asteroids)))
    if count > best_count:
        best_count = count
        best_asteroid = a

print(best_count)

asteroids.remove(best_asteroid)

for a in asteroids:
    a.angle_to_best = angle(best_asteroid, a)
    a.distance_to_best = distance(a, best_asteroid)

groups = itertools.groupby(sorted(asteroids, key=lambda a: a.angle_to_best), key=lambda a: a.angle_to_best)

sorted_groups = []

for k, v in groups:
    sorted_groups.append(sorted(list(v), key=lambda a: a.distance_to_best))

for i in range(0, len(sorted_groups)):
    group = sorted_groups[i]
    cur = group.pop(0)
    print(i+1, cur.x, cur.y)

