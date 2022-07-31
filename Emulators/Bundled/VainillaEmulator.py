from Emulators.OhNoAnotherBunchOfBrainFckEmulators4Python import ONABOBFE4P_emulation_standard


class ONABOBFE4P_emulation_plain(ONABOBFE4P_emulation_standard):
    """The most vainilla implementation fo ONABOBFE4P, it uses the default configuration and just reads the input and
    prints the results, no hooks are involved."""
    def __init__(self, program, initial_data=None):
        super().__init__(program, initial_data, hooks=[])


if __name__=="__main__":
    hello_world = "s>++++++++[<+++++++++>-]<.>++++[<+++++++>-]<+.+++++++..+++.>>++++++[<+++++++>-]<++.------------.>++++++[<+++++++++>-]<+.<.+++.------.--------.>>>++++[<++++++++>-]<+."
    ONABOBFE4P_emulation_plain(hello_world, None).run()