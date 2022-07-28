from OhNoAnotherBrainFckEmulator4Python import ONABFE4P_emulation_base

class Emulation_Test(ONABFE4P_emulation_base):

    def __init__(self, program, max_cell_value=8, use_negatives=False,
                 allow_pointer_overflow=False, allow_pointer_underflow=False,
                 allow_data_overflow=False, allow_data_underflow=False, input_stack=None):

        if input_stack is None: input_stack = []
        self.output_stack = []

        def print_default(x): self.output_stack.append(x)
        def input_default(): return input_stack.pop()

        super().__init__(program, None, max_data=8, hooks=[],
                         io_output=print_default, io_input=input_default,
                         max_cell_value=max_cell_value, use_negatives=use_negatives,
                         allow_pointer_overflow=allow_pointer_overflow, allow_pointer_underflow=allow_pointer_underflow,
                         allow_data_overflow=allow_data_overflow, allow_data_underflow=allow_data_underflow)