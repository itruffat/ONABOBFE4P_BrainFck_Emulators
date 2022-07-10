from OhNoAnotherTinyBrainFckEmulator import emulator_setup

class State:
    pass

state = State()
state.d = True
state.i = 0
state.always = False
state.cumulative =  []
state.do_continue = True


def print_peep_with_start(data, initial_data, max_data, data_pointer, program_pointer, program, program_jumps, input_buffer):
    global state
    if program_pointer < len(program):
        if program[program_pointer] == "s":
            state.d = True
        if program[program_pointer] == "h":
            state.d = False
        if program[program_pointer] == "a":
            state.always = True
        if program[program_pointer] == "n":
            state.always = False
    if state.d and state.do_continue:
        state.i += 1
        if state.always or state.i > 400 or program_pointer == len(program):
            state.i = 0
            print("@ " + "|".join(map(str,data[max(0,data_pointer-10):min(max_data,data_pointer+10)])))
            print(f"# data:{data_pointer} / program:{program_pointer} ({program[max(0,program_pointer-2):min(len(program),program_pointer+2)]}) {'END' if len(program)==program_pointer else program[program_pointer]}")


def cumulative_print(x):
    global state
    state.cumulative.append(x)
    n = ord(x)
    if 31 < n < 127:
        print(f"Output: {''.join(state.cumulative)}")
    else:
        if n == 7:
            state.do_continue = False
            print("Code to exit")
        else:
            print(f"Invalid control character")

def print_controls(intercept, initial_data, data, max_data, data_pointer, program_pointer, program, program_jumps,
                  input_buffer, print_f, input_f, peep, do_continue):
    global state
    return intercept, initial_data, data, max_data, data_pointer, program_pointer, program, program_jumps, input_buffer, print_f, input_f, peep, state.do_continue

emulator = emulator_setup(peep=print_peep_with_start, print_f=cumulative_print, intercept=print_controls)
