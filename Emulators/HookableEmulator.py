from abc import ABC
from OhNoAnotherBunchOfBrainFckEmulators4Python import ONABOBFE4P_emulation_standard

class ONABOBFE4P_emulation_with_generic_hooks(ONABOBFE4P_emulation_standard, ABC):
    """An example of how to use hooks, here you have 2 hooks:
    One of them only looks at the information (peep), whereas the other changes
    ever field (interceptor). My suggestion is to create your own and customize them
    by giving them the fields you actually need to intercept"""
    def __init__(self, program, initial_data=None, peep=None, interceptor=None):

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
                emulation.max_cell_value, \
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
                                               emulation.max_cell_value,
                                               do_continue)
            return do_continue, False

        def _run_peep(emulation, when, exception=None):
            if emulation.hook_peep is not None:
                emulation.hook_peep(when, exception, emulation.data, emulation.initial_data, emulation.max_data, emulation.data_pointer,
                                    emulation.program_pointer, emulation.program, emulation.input_buffer)
            return True, False

        super().__init__(program, initial_data, hooks= [_run_peep, _run_interceptor])