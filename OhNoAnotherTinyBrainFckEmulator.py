from abc import ABC


class ONATBFE_emulation_base(ABC):
    """
    Main definition, here is where most things run
    """

    def __init__(self, program, initial_data, max_data, hooks, io_output, io_input,max_cell_power):
        self.initial_config(program, initial_data, max_data, hooks, io_output, io_input, max_cell_power)

    def initial_config(self, program, initial_data, max_data, hooks , io_output, io_input, max_cell_power):
        self.data = [0 for _ in range(max_data)] if initial_data is None else initial_data
        assert (len(self.data) == max_data)
        self.data_pointer = 0
        self.program_pointer = 0
        self.input_buffer = []
        self.hooks = hooks
        self.io_output = io_output
        self.io_input = io_input
        self.max_cell_power = max_cell_power
        self.program = program
        self.initial_data = initial_data
        self.max_data = max_data

    def run(self):
        do_continue = True
        self._run_hooks("START")
        while do_continue and self.program_pointer < len(self.program):
            do_continue = self._step()
        self._run_hooks("DONE")

    def _run_hooks(self, when, exception=None):
        do_continue = True
        skip_exception = False
        for hook in self.hooks:
            t_do_continue, t_skip_exception = hook(self,when,exception)
            if t_do_continue is not None:
                do_continue = do_continue and t_do_continue
            if t_skip_exception is not None:
                skip_exception = skip_exception or t_skip_exception
        return do_continue, skip_exception

    def _step(self):
        try:
            do_continue, _ = self._run_hooks("START_STEP")
            if do_continue:
                n = self.program[self.program_pointer]
                if n == ">":
                    assert (self.data_pointer < len(self.data))
                    self._run_hooks(">")
                    self.data_pointer += 1
                elif n == "<":
                    assert (self.data_pointer > 0)
                    self._run_hooks("<")
                    self.data_pointer -= 1
                elif n == '+':
                    assert (self.data[self.data_pointer] < 2 ** self.max_cell_power)
                    self._run_hooks("+")
                    self.data[self.data_pointer] += 1
                elif n == '-':
                    assert (self.data[self.data_pointer] > 0)
                    self._run_hooks("-")
                    self.data[self.data_pointer] -= 1
                elif n == '[':
                    self._run_hooks("PRE[")
                    if self.data[self.data_pointer] == 0:
                        self._run_hooks("POST[")
                        depth = 0
                        while depth != 1 or self.program[self.program_pointer] != "]":
                            assert (self.program_pointer < self.max_data)
                            if self.program[self.program_pointer] == "[":
                                depth += 1
                            if self.program[self.program_pointer] == "]":
                                depth -= 1
                            self.program_pointer += 1
                elif n == ']':
                    self._run_hooks("PRE[")
                    if self.data[self.data_pointer] != 0:
                        self._run_hooks("POST[")
                        depth = 0
                        while depth != 1 or self.program[self.program_pointer] != "[":
                            assert (self.program_pointer >= 0)
                            if self.program[self.program_pointer] == "]":
                                depth += 1
                            if self.program[self.program_pointer] == "[":
                                depth -= 1
                            self.program_pointer -= 1
                elif n == '.':
                    self._run_hooks(".")
                    self.io_output(chr(self.data[self.data_pointer]))
                elif n == ',':
                    self._run_hooks(",")
                    while len(self.input_buffer) == 0:
                        self.input_buffer = list(self.io_input())
                    char = ord(self.input_buffer.pop(0))
                    self.data[self.data_pointer] = char
                self.program_pointer += 1
                do_continue, _ = self._run_hooks("END_STEP")
        except Exception as e:
            do_continue, skip_exception = self._run_hooks("ERROR", e)
            if not skip_exception:
                raise e

        return do_continue


class ONATBFE_emulation_basic(ONATBFE_emulation_base, ABC):
    """
    Subclass defined with the most common attributes, which I decided to use as default for my machines.
    This includes a simple input/output scheme, 3000 available pieces of data and 8 bits for each cell
    """
    def __init__(self, program, initial_data,hooks):
        def print_default(x): print(x, end='')
        def input_default(): return input()
        super().__init__(program, initial_data, max_data=3000, hooks = hooks, io_output= print_default, io_input=input_default, max_cell_power=8)