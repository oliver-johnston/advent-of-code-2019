import math


def execute_program(mem, input_func, output_func):
    pointer = 0
    while mem[pointer] != 99:

        instruction = mem[pointer]
        op_code = instruction % 100
        mode_1 = math.floor(instruction / 100) % 10
        mode_2 = math.floor(instruction / 1000) % 10
        mode_3 = math.floor(instruction / 10000) % 10

        num_parameters = 3
        if op_code in [3, 4]:
            num_parameters = 1
        if op_code in [5, 6]:
            num_parameters = 2

        parameter_1 = mem[pointer + 1] if num_parameters >= 1 else 0
        parameter_2 = mem[pointer + 2] if num_parameters >= 2 else 0
        parameter_3 = mem[pointer + 3] if num_parameters >= 3 else 0

        value_1 = mem[parameter_1] if mode_1 == 0 else parameter_1
        value_2 = mem[parameter_2] if mode_2 == 0 else parameter_2
        value_3 = mem[parameter_3] if mode_3 == 0 else parameter_3

        update_pointer = True

        if op_code == 1:
            mem[parameter_3] = value_1 + value_2
        elif op_code == 2:
            mem[parameter_3] = value_1 * value_2
        elif op_code == 3:
            mem[parameter_1] = input_func()
        elif op_code == 4:
            output_func(mem[parameter_1])
        elif op_code == 5:
            if value_1 != 0:
                pointer = value_2
                update_pointer = False
        elif op_code == 6:
            if value_1 == 0:
                pointer = value_2
                update_pointer = False
        elif op_code == 7:
            mem[parameter_3] = 1 if value_1 < value_2 else 0
        elif op_code == 8:
            mem[parameter_3] = 1 if value_1 == value_2 else 0
        else:
            raise Exception("Invalid op_code: " + str(op_code))

        if update_pointer:
            pointer += num_parameters + 1