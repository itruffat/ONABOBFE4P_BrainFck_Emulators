from OhNoAnotherTinyBrainFckEmulator import ONATBFE_emulation_basic

class ONATBFE_emulation_plain(ONATBFE_emulation_basic):
    """The most vainilla implementation fo ONATBFE, it uses the default configuration and just reads the input and
    prints the results, no hooks are involved."""
    def __init__(self, program, initial_data):
        super().__init__(program, initial_data, hooks=[])


class ONATBFE_emulation_with_generic_hooks(ONATBFE_emulation_basic):
    """An example of how to use hooks, here you have 2 hooks:
    One of them only looks at the information (peep), whereas the other changes
    ever field (interceptor). My suggestion is to create your own and customize them
    by giving them the fields you actually need to intercept"""
    def __init__(self, program, initial_data, peep=None, interceptor=None):

        self.hook_peep = peep
        self.hook_intercept = interceptor

        def _run_interceptor(emulation, when, exception=None):
            do_continue = True
            if emulation.hook_intercept is not None:
                emulation.hook_intercept, \
                emulation.initial_data, \
                emulation.data, \
                emulation.max_data, \
                emulation.data_pointer, \
                emulation.program_pointer, \
                emulation.program, \
                emulation.input_buffer, \
                emulation.io_output, \
                emulation.io_input, \
                emulation.hook_peep, \
                emulation.max_cell_power, \
                do_continue, \
                exception \
                    = emulation.hook_intercept(when,
                                               exception,
                                               emulation.hook_intercept,
                                               emulation.initial_data,
                                               emulation.data,
                                               emulation.max_data,
                                               emulation.data_pointer,
                                               emulation.program_pointer,
                                               emulation.program,
                                               emulation.input_buffer,
                                               emulation.io_output,
                                               emulation.io_input,
                                               emulation.hook_peep,
                                               emulation.max_cell_power,
                                               do_continue)
            return do_continue, False

        def _run_peep(emulation, when, exception=None):
            if emulation.hook_peep is not None:
                emulation.hook_peep(when, exception, emulation.data, emulation.initial_data, emulation.max_data, emulation.data_pointer,
                                    emulation.program_pointer, emulation.program, emulation.input_buffer)
            return True, False

        super().__init__(program, initial_data, hooks= [_run_peep, _run_interceptor])


class ONATBFE_emulation_with_statefull_print(ONATBFE_emulation_with_generic_hooks):
    """Sometimes it's important to look at the memory"""

    def __init__(self, program, initial_data):

        self.peep_started= False
        self.peep_always = False
        self.peep_steps = 0
        self.old_prints = []

        def peep(when, exception, data, initial_data, max_data, data_pointer,
                                    program_pointer, program,input_buffer):
            if exception is None and when in ["START_STEP", "DONE"]:
                if program_pointer < len(program):
                    if program[program_pointer] == "s":
                        self.peep_started = True
                    if program[program_pointer] == "h":
                        self.peep_started = False
                    if program[program_pointer] == "a":
                        self.peep_always = True
                    if program[program_pointer] == "n":
                        self.peep_always = False
                if self.peep_started:
                    self.peep_steps += 1
                    if self.peep_always or self.peep_steps > 100 or program_pointer == len(program):
                        self.peep_steps = 0
                        print("@ " + "|".join(map(str, data[max(0, data_pointer - 10):min(max_data, data_pointer + 10)])))
                        print(
                            f"# data:{data_pointer} / program:{program_pointer} ({program[max(0, program_pointer - 2):min(len(program), program_pointer + 2)]}) {'END' if len(program) == program_pointer else program[program_pointer]}")

        def print_with_memory(x):
            self.old_prints.append(x)
            print("".join(self.old_prints))

        super().__init__(program,initial_data,peep=peep, interceptor=None)
        self.io_output = print_with_memory


hello_world = "s>++++++++[<+++++++++>-]<.>++++[<+++++++>-]<+.+++++++..+++.>>++++++[<+++++++>-]<++.------------.>++++++[<+++++++++>-]<+.<.+++.------.--------.>>>++++[<++++++++>-]<+."

ONATBFE_emulation_with_statefull_print(hello_world, None).run()