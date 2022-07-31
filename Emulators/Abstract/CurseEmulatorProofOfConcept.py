from abc import ABC
from Emulators.OhNoAnotherBunchOfBrainFckEmulators4Python import ONABOBFE4P_emulation_base
from Emulators.Abstract.CurseEmulatorEngine import start_curse_engine, start_curse_queues, queues
from time import sleep

class ONABOBFE4P_emulation_using_curse_POC(ONABOBFE4P_emulation_base, ABC):
    def __init__(self, program, initial_data=None):

        start_curse_queues()

        self.input_queue = queues.input
        self.output_queue = queues.output
        self.shutdown_queue = queues.shutdown

        def print_curse(x):
            self.output_queue.put(x)

        def input_curse():
            input_char = None
            while input_char is None:
                if not self.input_queue.empty():
                    input_char = chr(self.input_queue.get())
            return [input_char]

        def finish_curse_when_program_done(self,when,error):
            if when == "DONE":
                sleep(4)
                self.shutdown_queue.put(1)
            return True, False

        super().__init__(program, initial_data, max_data=30000, hooks=[finish_curse_when_program_done],
                         io_output=print_curse, io_input=input_curse,
                         max_cell_value=2 ** 8, use_negatives=False,
                         allow_pointer_overflow=False, allow_pointer_underflow=False,
                         allow_data_overflow=False, allow_data_underflow=False)

    def run(self):
        try:
            start_curse_engine()
            super().run()
        except Exception as e:
            self.shutdown_queue.put(1)
            raise e

if __name__ == "__main__":
    input_output = ",.++.>,.<."
    ONABOBFE4P_emulation_using_curse_POC(input_output, None).run()