from functools import partial


def calculate_jumps(program, program_jumps, position=0, depth=0):
    while position < len(program):
        if program[position] == ']':
            assert (depth > 0)
            return position
        if program[position] == '[':
            close_position = calculate_jumps(program, program_jumps, position+1, depth+1)
            program_jumps[position] = close_position
            program_jumps[close_position] = position
            position = close_position
        position += 1
    assert(position == len(program))
    assert(depth == 0)


def run(program, initial_data, max_data, peep, intercept, print_f, input_f ):
    data = [0 for _ in range(max_data)] if initial_data is None else initial_data
    assert(len(data) == max_data)
    data_pointer = 0
    program_pointer = 0
    program_jumps = {}
    calculate_jumps(program, program_jumps)
    input_buffer = []
    do_continue = True
    while program_pointer < len(program):
        if intercept is not None:
            intercept, initial_data, data, max_data, data_pointer, program_pointer, program, program_jumps, input_buffer, print_f, input_f, peep, do_continue = \
                intercept(intercept, initial_data, data, max_data, data_pointer, program_pointer, program, program_jumps, input_buffer, print_f, input_f, peep, do_continue)
        if not do_continue:
            break
        if peep is not None:
            peep(data, initial_data, max_data, data_pointer, program_pointer, program, program_jumps, input_buffer)
        n = program[program_pointer]
        if n == ">":
            assert (data_pointer < len(data))
            data_pointer += 1
        elif n == "<":
            assert(data_pointer > 0)
            data_pointer -= 1
        elif n == '+':
            assert(data[data_pointer] < 2**16)
            data[data_pointer] += 1
        elif n == '-':
            assert(data[data_pointer] > 0)
            data[data_pointer] -= 1
        elif n == '[':
            if data[data_pointer] == 0:
                program_pointer = program_jumps[program_pointer]
        elif n == ']':
            if data[data_pointer] != 0:
                program_pointer = program_jumps[program_pointer]
        elif n == '.':
            print_f(chr(data[data_pointer]))
        elif n == ',':
            while len(input_buffer) == 0:
                input_buffer = list(input_f())
            char = ord(input_buffer.pop(0))
            data[data_pointer] = char
        program_pointer += 1
    if peep is not None:
        peep(data, initial_data, max_data, data_pointer, program_pointer, program, program_jumps, input_buffer)


max_data_default = 3000
input_f_default = input
def print_f_default(x): print(x, end='')


def emulator_setup(
        initial_data=None, max_data=max_data_default,
        peep=None, intercept=None,
        print_f=print_f_default, input_f=input_f_default):
    return partial(run,
                   initial_data=initial_data, max_data=max_data,
                   peep=peep, intercept=intercept,
                   print_f=print_f, input_f=input_f)