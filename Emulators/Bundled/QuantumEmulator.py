from Emulators.Abstract.HookableEmulator import ONABOBFE4P_emulation_with_generic_hooks


class ONABOBFE4P_emulation_with_quantum(ONABOBFE4P_emulation_with_generic_hooks):
    """Quantum to enable hardware~ish emulation"""

    def __init__(self, program, initial_data=None, quantum_map=None):

        if quantum_map is None:
            quantum_map = {
                ">": 0,
                "<": 0,
                "+": 0,
                "-": 0,
                "[": 0,
                "]": 0,
                ".": 0,
                ",": 0
            }
        else:
            for i in [">", "<", "+", "-", "[", "]", ".", ","]:
                assert (i in quantum_map)

        self.quantum_map = quantum_map
        self.quantum = -1
        self.program_total_quantum = 0

        def quantum_checker(when,
                            exception,
                            hook_intercept,
                            initial_data,
                            data,
                            max_data,
                            data_pointer,
                            program_pointer,
                            program,
                            input_buffer,
                            io_output,
                            io_input,
                            hook_peep,
                            max_cell_value,
                            do_continue):

            if exception is not None or when != "START_STEP" or program[program_pointer] not in self.quantum_map.keys():
                return hook_intercept, \
                       initial_data, \
                       data, \
                       max_data, \
                       data_pointer, \
                       program_pointer, \
                       program, \
                       input_buffer, \
                       io_output, \
                       io_input, \
                       hook_peep, \
                       max_cell_value, \
                       do_continue, \
                       exception
            else:
                if self.quantum < 0:
                    self.quantum = self.quantum_map[program[program_pointer]]
                self.quantum -= 1
                self.program_total_quantum += 1
                if self.quantum < 0:
                    consumed_enough_quantum_to_continue = True
                else:
                    consumed_enough_quantum_to_continue = False
                return hook_intercept, \
                       initial_data, \
                       data, \
                       max_data, \
                       data_pointer, \
                       program_pointer, \
                       program, \
                       input_buffer, \
                       io_output, \
                       io_input, \
                       hook_peep, \
                       max_cell_value, \
                       consumed_enough_quantum_to_continue, \
                       exception

        super().__init__(program, initial_data, peep=None, interceptor=quantum_checker)

    def _step(self):
        do_continue = super()._step()
        do_continue = do_continue or self.quantum > -1
        return do_continue

    def run(self):
        self._run_with_step(self._step)
        print(f'\nTotal_quantum: {self.program_total_quantum}')



if __name__ == "__main__":
    hello_world = "s>++++++++[<+++++++++>-]<.>++++[<+++++++>-]<+.+++++++..+++.>>++++++[<+++++++>-]<++.------------.>++++++[<+++++++++>-]<+.<.+++.------.--------.>>>++++[<++++++++>-]<+."

    hello_world_qm = {
        ">": 1,
        "<": 1,
        "+": 2,
        "-": 2,
        "[": 14,
        "]": 3,
        ".": 1,
        ",": 100
    }
    ONABOBFE4P_emulation_with_quantum(hello_world, None, hello_world_qm).run()
