import curses
import intcode
import math
from time import sleep
from curses import wrapper
from random import random


class Droid:
    def __init__(self, program, stdscr):
        self.program = program
        self.direction = 1
        self.found_oxygen = False
        self.flooding = False
        self.distances = dict()
        self.has_oxygen = dict()
        self.walls = set()

        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)
        stdscr.keypad(True)

        self.stdscr = stdscr
        self.win = curses.newwin(curses.LINES - 1, curses.COLS - 1, 0, 0)
        self.x = curses.COLS // 2
        self.y = curses.LINES // 2

        self.origin_x = self.x
        self.origin_y = self.y
        self.distances[(self.x, self.y)] = 0
        self.has_oxygen[(self.x, self.y)] = False
        self.repair_x = 0
        self.repair_y = 0
        self.win.addch(self.y, self.x, "D")

    def store_output(self, o):
        next_x = self.next_x()
        next_y = self.next_y()

        if o == 0:
            self.win.addch(next_y, next_x, "#")
            self.walls.add((next_x, next_y))
        else:
            self.win.addch(self.y, self.x, ".")

            distance = self.distances.get((self.x, self.y)) + 1
            distance_next = self.distances.get((next_x, next_y), 999999)

            self.x = next_x
            self.y = next_y

            self.distances[(self.x, self.y)] = min(distance, distance_next)
            self.has_oxygen[(self.x, self.y)] = False

        if o == 2:
            self.repair_x = self.x
            self.repair_y = self.y
            self.has_oxygen[(self.x, self.y)] = True
            self.found_oxygen = True

        self.change_direction()

        self.win.addch(self.y, self.x, "D")

        if self.found_oxygen:
            self.win.addch(self.repair_y, self.repair_x, "O")
            self.win.addstr(0, 0, "Distance to oxygen: " + str(self.distances[(self.repair_x, self.repair_y)]))
            self.win.addstr(1, 0, "Press any key to start flooding with oxygen")

            self.win.nodelay(True)
            if self.win.getch() != curses.ERR:
                self.flooding = True

        self.win.refresh()

    def next_x(self):
        if self.direction == 3:
            return self.x - 1
        if self.direction == 4:
            return self.x + 1
        return self.x

    def next_y(self):
        if self.direction == 1:
            return self.y - 1
        if self.direction == 2:
            return self.y + 1
        return self.y

    def change_direction(self):
        up = (self.x, self.y - 1)
        down = (self.x, self.y + 1)
        west = (self.x - 1, self.y)
        east = (self.x + 1, self.y)

        direction = math.ceil(random()*4)
        # if there is somewhere we haven't visited then go there, otherwise just random
        # not perfect but if you wait long enough it works
        for i in range(0, 4):
            direction = (direction % 4) + 1
            if direction == 1 and up not in self.walls and up not in self.has_oxygen:
                break
            if direction == 2 and down not in self.walls and down not in self.has_oxygen:
                break
            if direction == 3 and west not in self.walls and west not in self.has_oxygen:
                break
            if direction == 4 and east not in self.walls and east not in self.has_oxygen:
                break

        self.direction = direction

    def get_input(self):
        if self.flooding:
            return 99
        return self.direction

    def run(self):
        intcode.execute_program(self.program, self.get_input, self.store_output)
        self.flood()
        sleep(100)

    def flood(self):
        i = 0
        while not all(self.has_oxygen.values()):
            to_flood = list(filter(self.should_flood, self.has_oxygen.keys()))
            for coord in to_flood:
                self.has_oxygen[coord] = True
                self.win.addch(coord[1], coord[0], "O")
            self.win.refresh()
            i += 1
            sleep(0.05)
            self.win.addstr(1, 0, "Flooding: " + str(i) + " minutes                        ")

        self.win.addstr(1, 0, "Flooded in " + str(i) + " minutes")
        self.win.refresh()

    def should_flood(self, coord):
        return (self.has_oxygen.get((coord[0] + 1, coord[1]))
                or self.has_oxygen.get((coord[0], coord[1] + 1))
                or self.has_oxygen.get((coord[0] - 1, coord[1]))
                or self.has_oxygen.get((coord[0], coord[1] - 1)))


def run(stdscr):
    fp = open("15.txt")
    data = list(map(lambda x: int(x), fp.read().split(",")))
    droid = Droid(data, stdscr)
    droid.run()


wrapper(run)
