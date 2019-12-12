import intcode
import threading


class Amp:
    def __init__(self, phase, program):
        self.output_amp = None
        self.inputs = [phase]
        self.program = program
        self.output = 0
        self.cv = threading.Condition()
        self.thread = threading.Thread(target=intcode.execute_program,
                                       args=(self.program,
                                             self.get_input,
                                             self.store_output))

    def get_input(self):
        with self.cv:
            while len(self.inputs) == 0:
                self.cv.wait()
            return self.inputs.pop(0)

    def store_output(self, output):
        self.output = output
        if self.output_amp is not None:
            self.output_amp.receive_input(output)

    def receive_input(self, next_input):
        with self.cv:
            self.inputs.append(next_input)
            self.cv.notify_all()

    def start(self):
        self.thread.start()


def run_amps(phases, program, feedback_loop):
    amps = []
    for phase in phases:
        amp = Amp(phase, program)
        amps.append(amp)
        amps[len(amps)-2].output_amp = amp

    first_amp = amps[0]
    last_amp = amps[len(amps) - 1]

    if feedback_loop:
        last_amp.output_amp = first_amp

    for amp in amps:
        amp.start()

    first_amp.receive_input(0)
    last_amp.thread.join()

    return last_amp.output


program = [3, 8, 1001, 8, 10, 8, 105, 1, 0, 0, 21, 42, 67, 88, 101, 114, 195, 276, 357, 438, 99999, 3, 9, 101, 3, 9,
           9, 1002, 9, 4, 9, 1001, 9, 5, 9, 102, 4, 9, 9, 4, 9, 99, 3, 9, 1001, 9, 3, 9, 1002, 9, 2, 9, 101, 2, 9, 9,
           102, 2, 9, 9, 1001, 9, 5, 9, 4, 9, 99, 3, 9, 102, 4, 9, 9, 1001, 9, 3, 9, 102, 4, 9, 9, 101, 4, 9, 9, 4, 9,
           99, 3, 9, 101, 2, 9, 9, 1002, 9, 3, 9, 4, 9, 99, 3, 9, 101, 4, 9, 9, 1002, 9, 5, 9, 4, 9, 99, 3, 9, 102, 2,
           9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 101, 1,
           9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2,
           9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 99, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001,
           9, 1, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 1001,
           9, 2, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 99, 3, 9,
           102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9,
           1001, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9,
           101, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 99, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3,
           9, 1001, 9, 1, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9,
           1001, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 99, 3,
           9, 1001, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3,
           9, 1002, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3,
           9, 101, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 99]

max_output = 0
for a in range(0, 5):
    for b in range(0, 5):
        for c in range(0, 5):
            for d in range(0, 5):
                for e in range(0, 5):
                    phases = [a, b, c, d, e]
                    if len(set(phases)) == len(phases):
                        max_output = max(max_output, run_amps(phases, program, False))

print(max_output)

max_output = 0
for a in range(5, 10):
    for b in range(5, 10):
        for c in range(5, 10):
            for d in range(5, 10):
                for e in range(5, 10):
                    phases = [a, b, c, d, e]
                    if len(set(phases)) == len(phases):
                        max_output = max(max_output, run_amps(phases, program, True))

print(max_output)
