import intcode


class Springdroid:
    def __init__(self, instructions):
        self.instruction_chars = list("\n".join(instructions)) + ["\n"]

    def run(self):
        intcode.execute_program(self.get_program(), self.get_input, self.write_output)

    def get_input(self):
        ch = self.instruction_chars.pop(0)
        return ord(ch)

    @staticmethod
    def get_program():
        fp = open("21.txt")
        return [int(x) for x in fp.read().split(",")]

    @staticmethod
    def write_output(o):
        if o > 1000:
            print(o)
        else:
            print(chr(o), end="")


Springdroid(["OR A J",  # J = land at A
             "AND C J", # J = land at A and C
             "NOT J J", # J = hole at A or C
             "AND D J", # J = (hole at A or C) and land at D
             "WALK"]).run()

Springdroid(["OR A J",  # J = land at A
             "AND B J", # J = land at A and B
             "AND C J", # J = land at A and B and C
             "NOT J J", # J = hole at A or B or C
             "AND D J", # J = (hole at A or B or C) and land at D
             "OR E T",  # T = land at E
             "OR H T",  # T = land at E or H
             "AND T J", # J = (hole at A or B or C) and land at D and (land at E or H)
             "RUN"]).run()
