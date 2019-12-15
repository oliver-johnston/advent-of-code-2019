import curses
import intcode
from time import sleep
from curses import wrapper
from enum import Enum


class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


class Location:
    def __init__(self, x, y, distance_from_origin):
        self.x = x
        self.y = y
        self.distance_from_origin = distance_from_origin
        self.has_oxygen = False


def turn_left(d):
    if d == Direction.NORTH:
        return Direction.WEST
    if d == Direction.SOUTH:
        return Direction.EAST
    if d == Direction.WEST:
        return Direction.SOUTH
    return Direction.NORTH


def turn_right(d):
    if d == Direction.NORTH:
        return Direction.EAST
    if d == Direction.SOUTH:
        return Direction.WEST
    if d == Direction.WEST:
        return Direction.NORTH
    return Direction.SOUTH


class Droid:
    def __init__(self, program, stdscr):
        self.program = program
        self.flooding = False

        self.stdscr = stdscr
        self.win = curses.newwin(curses.LINES - 1, curses.COLS - 1, 0, 0)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)
        stdscr.keypad(True)

        origin = Location(curses.COLS // 2, curses.LINES // 2, 0)
        self.locations = dict()
        self.location = origin
        self.locations[(origin.x, origin.y)] = origin

        self.oxygen = None

        self.desired_direction = Direction.NORTH
        self.actual_direction = Direction.NORTH

    def store_output(self, o):
        cur_location = self.location
        next_location = self.next_location()

        if o == 0:
            # hit a wall
            self.win.addch(next_location.y, next_location.x, "#")
            if self.desired_direction == self.actual_direction:
                # hit a wall when travelling in desired direction, turn fully left
                self.actual_direction = turn_left(self.desired_direction)
                self.desired_direction = self.actual_direction
            else:
                # hit a wall when testing a direction, turn back to the desired direction
                self.actual_direction = self.desired_direction
        else:
            # moved forward
            self.win.addch(cur_location.y, cur_location.x, ".")
            self.location = next_location
            self.locations[(next_location.x, next_location.y)] = next_location

            next_location.distance_from_origin = min(next_location.distance_from_origin,
                                                     cur_location.distance_from_origin + 1)

            # test moving right
            self.desired_direction = self.actual_direction
            self.actual_direction = turn_right(self.actual_direction)

        if o == 2:
            self.location.has_oxygen = True
            self.oxygen = self.location

        if self.oxygen is not None:
            self.win.addch(self.oxygen.y, self.oxygen.x, "O")
            self.win.addstr(0, 0, "Distance to oxygen: " + str(self.oxygen.distance_from_origin))
            self.win.addstr(1, 0, "Press any key to start flooding with oxygen")

            self.win.nodelay(True)
            if self.win.getch() != curses.ERR:
                self.flooding = True

        self.win.addch(self.location.y, self.location.x, "D")
        self.win.refresh()

    def next_location(self):
        x = self.location.x
        y = self.location.y

        if self.actual_direction == Direction.NORTH:
            y -= 1
        elif self.actual_direction == Direction.SOUTH:
            y += 1
        elif self.actual_direction == Direction.WEST:
            x -= 1
        elif self.actual_direction == Direction.EAST:
            x += 1

        return self.locations.get((x, y), Location(x, y, 99999))

    def get_input(self):
        if self.flooding:
            return 99

        sleep(0.003)
        return self.actual_direction.value

    def run(self):
        intcode.execute_program(self.program, self.get_input, self.store_output)
        self.flood()
        sleep(100)

    def flood(self):
        i = 0
        while not all(map(lambda x: x.has_oxygen, self.locations.values())):
            to_flood = list(filter(self.should_flood, self.locations.values()))
            for location in to_flood:
                location.has_oxygen = True
                self.win.addch(location.y, location.x, "O")
            i += 1
            self.win.addstr(1, 0, "Flooding: " + str(i) + " minutes                        ")
            self.win.refresh()
            sleep(0.02)

        self.win.addstr(1, 0, "Flooded in " + str(i) + " minutes")
        self.win.refresh()

    def should_flood(self, location):
        n = self.locations.get((location.x, location.y - 1))
        e = self.locations.get((location.x - 1, location.y))
        s = self.locations.get((location.x, location.y + 1))
        w = self.locations.get((location.x + 1, location.y))

        return ((n is not None and n.has_oxygen)
                or (s is not None and s.has_oxygen)
                or (e is not None and e.has_oxygen)
                or (w is not None and w.has_oxygen))


def run(stdscr):
    fp = open("15.txt")
    data = list(map(lambda x: int(x), fp.read().split(",")))
    droid = Droid(data, stdscr)
    droid.run()


wrapper(run)
