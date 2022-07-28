from abc import ABC


class ONABFE4P_emulation_base(ABC):
    """
    Main class, here is where most things run.
     * program: The BF program to be run, it must be an string.
     * initial_data: A way to initialize the array for testing. It's not compulsory and if left as "None" it will be
                     automatically filled with zeros. It must always have a length equal to max_data.
     * max_data: The size of the data stack.
     * hooks: Functions that are called during certain parts of the execution. Subclasses can have their own hooks to
              customize how things are called.
     * io_output: Function that will handle how data is given to the user of the program.
     * io_input: Function that will handle how data will be received from the user.
     * max_cell_value: Variable that says what is the max_value the data blocks can have.
                       If left as "None", then an infinitely large piece of data can be used.
     * use_negatives: Allows the use of negative data values.
     * allow_pointer_overflow: Allows the data pointer to wrap around and go from (max_data -1) to 0.
     * allow_pointer_underflow: Allows the data pointer to wrap around and go from 0 to (max_data-1).
     * allow_data_overflow: Allows data to wrap around, and go from the biggest possible value to the smallest one.
                            Has no use if max_cell_value is "None", since it can not overflow.
     * allow_data_underflow: Allows data to wrap around, and go from the smallest possible value to the biggest one.
                            Has no use if max_cell_value is "None", since it can not pick a value to go after underflow.
    """

    def __init__(self, program, initial_data, max_data, hooks, io_output, io_input, max_cell_value, use_negatives,
                 allow_pointer_overflow, allow_pointer_underflow, allow_data_overflow, allow_data_underflow):
        self.initial_config(program, initial_data, max_data, hooks, io_output, io_input, max_cell_value, use_negatives,
                            allow_pointer_overflow, allow_pointer_underflow, allow_data_overflow, allow_data_underflow)

    def initial_config(self, program, initial_data, max_data, hooks, io_output, io_input, max_cell_value,
                       use_negatives, allow_pointer_overflow, allow_pointer_underflow, allow_data_overflow,
                       allow_data_underflow):
        self.data = [0 for _ in range(max_data)] if initial_data is None else initial_data
        assert (len(self.data) == max_data)
        self.data_pointer = 0
        self.program_pointer = 0
        self.input_buffer = []
        self.hooks = hooks
        self.io_output = io_output
        self.io_input = io_input
        self.max_cell_value = max_cell_value
        self.program = program
        self.initial_data = initial_data
        self.max_data = max_data
        self.use_negatives = use_negatives
        self.allow_pointer_overflow = allow_pointer_overflow
        self.allow_pointer_underflow = allow_pointer_underflow
        self.allow_data_overflow = allow_data_overflow
        self.allow_data_underflow = allow_data_underflow

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
            t_do_continue, t_skip_exception = hook(self, when, exception)
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
                    # Overflow check
                    assert (self.allow_pointer_overflow or self.data_pointer < len(self.data))
                    do_continue, _ = self._run_hooks(">")
                    if do_continue:
                        self.data_pointer += 1
                        # Overflow control
                        if self.data_pointer > len(self.data) - 1:
                            self.data_pointer = 0
                elif n == "<":
                    # Underflow check
                    assert (self.allow_pointer_underflow or self.data_pointer > 0)
                    do_continue, _ = self._run_hooks("<")
                    if do_continue:
                        self.data_pointer -= 1
                        # Underflow control
                        if self.data_pointer < 0:
                            self.data_pointer = self.max_data - 1
                elif n == '+':
                    # Overflow check
                    assert (self.allow_data_overflow or self.max_cell_value is None or
                            self.data[self.data_pointer] < (self.max_cell_value)-1)
                    do_continue,_ = self._run_hooks("+")
                    if do_continue:
                        self.data[self.data_pointer] += 1
                        # Overflow control
                        if (self.max_cell_value is not None and
                                self.data[self.data_pointer] > (self.max_cell_value) - 1):
                            if self.use_negatives:
                                self.data[self.data_pointer] = -(self.max_cell_value) + 1
                            else:
                                self.data[self.data_pointer] = 0
                elif n == '-':
                    # Underflow check
                    assert (
                            (self.max_cell_value is None and self.use_negatives) or
                            (self.allow_data_underflow and self.max_cell_value is not None) or
                            (self.use_negatives and self.data[self.data_pointer] > -(self.max_cell_value)+1) or
                            (not self.use_negatives and self.data[self.data_pointer] > 0))
                    do_continue, _ = self._run_hooks("-")
                    if do_continue:
                        self.data[self.data_pointer] -= 1
                        # Underflow control
                        if self.max_cell_value is not None:
                            if ((self.use_negatives and self.data[self.data_pointer] < -(self.max_cell_value)+1) or
                                    (not self.use_negatives and self.data[self.data_pointer] < 0)):
                                self.data[self.data_pointer] = (self.max_cell_value) - 1
                elif n == '[':
                    do_continue, _ = self._run_hooks("PRE[")
                    if do_continue and self.data[self.data_pointer] == 0:
                        do_continue, _ = self._run_hooks("POST[")
                        if do_continue:
                            depth = 0
                            while depth != 1 or self.program[self.program_pointer] != "]":
                                assert (self.program_pointer < self.max_data)
                                if self.program[self.program_pointer] == "[":
                                    depth += 1
                                if self.program[self.program_pointer] == "]":
                                    depth -= 1
                                self.program_pointer += 1
                elif n == ']':
                    do_continue, _ = self._run_hooks("PRE[")
                    if do_continue and self.data[self.data_pointer] != 0:
                        do_continue, _ = self._run_hooks("POST[")
                        if do_continue:
                            depth = 0
                            while depth != 1 or self.program[self.program_pointer] != "[":
                                assert (self.program_pointer >= 0)
                                if self.program[self.program_pointer] == "]":
                                    depth += 1
                                if self.program[self.program_pointer] == "[":
                                    depth -= 1
                                self.program_pointer -= 1
                elif n == '.':
                    do_continue, _ = self._run_hooks(".")
                    if do_continue:
                        char = chr(self.data[self.data_pointer])
                        self.io_output(char)
                elif n == ',':
                    do_continue, _ = self._run_hooks(",")
                    if do_continue:
                        while len(self.input_buffer) == 0:
                            self.input_buffer = list(self.io_input())
                        char = ord(self.input_buffer.pop(0))
                        self.data[self.data_pointer] = char
                if do_continue:
                    self.program_pointer += 1
                    do_continue, _ = self._run_hooks("END_STEP")
        except Exception as e:
            do_continue, skip_exception = self._run_hooks("ERROR", e)
            if not skip_exception:
                raise e

        return do_continue


class ONABFE4P_emulation_standard(ONABFE4P_emulation_base, ABC):
    """
    Subclass defined with the most common attributes, which I decided to use as default for my machines.
    This includes a simple input/output scheme, 30000 available pieces of data and 8 bits for each cell
    """

    def __init__(self, program, initial_data, hooks):
        def print_default(x): print(x, end='')

        def input_default(): return input()

        super().__init__(program, initial_data, max_data=30000, hooks=hooks,
                         io_output=print_default, io_input=input_default,
                         max_cell_value=2**8, use_negatives=False,
                         allow_pointer_overflow=False, allow_pointer_underflow=False,
                         allow_data_overflow=False, allow_data_underflow=False)
