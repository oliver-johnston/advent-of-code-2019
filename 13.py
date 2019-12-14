import intcode
import curses
from time import sleep
from curses import wrapper


class ArcadeCabinet:
    def __init__(self, program, stdscr):
        self.program = program
        self.index = 0
        self.x = 0
        self.y = 0
        self.tile_id = 0
        self.score = 0
        self.input_ch = 0

        self.paddle_x = 0
        self.ball_x = 0

        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)
        stdscr.keypad(True)
        self.stdscr = stdscr
        self.win = curses.newwin(curses.LINES - 1, curses.COLS - 1, 0, 0)

        self.chars = [" ", "#", ".", "-", "o"]

    def store_output(self, o):
        if self.index == 0:
            self.x = o
        elif self.index == 1:
            self.y = o
        else:
            self.tile_id = o
            if self.x == -1 and self.y == 0:
                self.score = self.tile_id
                self.update_score()
            else:
                self.update_screen()

            if self.tile_id == 3:
                self.paddle_x = self.x
            elif self.tile_id == 4:
                self.ball_x = self.x

        self.index = (self.index + 1) % 3

    def update_score(self):
        self.win.addstr(0, 60, "Score: " + str(self.score) + "     ")
        self.win.refresh()

    def update_screen(self):
        self.win.addch(self.y, self.x, self.chars[self.tile_id])
        self.win.refresh()

    def get_input(self):
        # uncomment to play the game
        # self.win.nodelay(True)
        # self.input_ch = self.win.getch()
        # sleep(0.5)
        # if self.input_ch == curses.KEY_LEFT or self.input_ch == ord('a'):
        #     return -1
        # elif self.input_ch == curses.KEY_RIGHT or self.input_ch == ord('d'):
        #     return 1
        if self.paddle_x < self.ball_x:
            return 1
        elif self.paddle_x > self.ball_x:
            return -1
        return 0

    def run(self):
        intcode.execute_program(self.program, self.get_input, self.store_output)

        self.win.nodelay(False)
        self.win.addstr(10, 55, "GAME OVER")
        self.win.addstr(11, 50, "(press any key to exit)")
        self.win.getch()

        curses.nocbreak()
        curses.curs_set(True)
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()


def play(stdscr):
    fp = open("13.txt")
    data = list(map(lambda x: int(x), fp.read().split(",")))
    data[0] = 2
    arcade = ArcadeCabinet(data, stdscr)
    arcade.run()


wrapper(play)
