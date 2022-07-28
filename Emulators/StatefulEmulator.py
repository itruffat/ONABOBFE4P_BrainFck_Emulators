from Emulators.HookableEmulator import ONABFE4P_emulation_with_generic_hooks

class ONABFE4P_emulation_with_statefull_print(ONABFE4P_emulation_with_generic_hooks):
    """Sometimes it's important to look at the memory"""

    def __init__(self, program, initial_data=None):

        self.peep_started= False
        self.peep_always = False
        self.peep_steps = 0
        self.old_prints = []

        def peep(when, exception, data, initial_data, max_data, data_pointer, program_pointer, program,input_buffer):
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

if __name__=="__main__":
    ONABFE4P_emulation_with_statefull_print(hello_world, None).run()