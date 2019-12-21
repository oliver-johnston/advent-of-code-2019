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


Springdroid(["OR A J",
             "AND C J",
             "NOT J J",
             "AND D J",
             "WALK"]).run()

Springdroid(["OR A J",
             "AND B J",
             "AND C J",
             "NOT J J",
             "AND D J",
             "OR E T",
             "OR H T",
             "AND T J",
             "RUN"]).run()
