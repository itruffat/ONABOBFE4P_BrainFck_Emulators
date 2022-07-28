from OhNoAnotherBrainFckEmulator4Python import ONABFE4P_emulation_standard


class ONABFE4P_emulation_plain(ONABFE4P_emulation_standard):
    """The most vainilla implementation fo ONABFE4P, it uses the default configuration and just reads the input and
    prints the results, no hooks are involved."""
    def __init__(self, program, initial_data):
        super().__init__(program, initial_data, hooks=[])


hello_world = "s>++++++++[<+++++++++>-]<.>++++[<+++++++>-]<+.+++++++..+++.>>++++++[<+++++++>-]<++.------------.>++++++[<+++++++++>-]<+.<.+++.------.--------.>>>++++[<++++++++>-]<+."

ONABFE4P_emulation_plain(hello_world, None).run()