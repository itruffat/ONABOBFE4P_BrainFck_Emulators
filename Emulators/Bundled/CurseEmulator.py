from Emulators.OhNoAnotherBunchOfBrainFckEmulators4Python import ONABOBFE4P_emulation_base
import curses
import os
from threading import Thread
from time import sleep, time
from queue import Queue, Empty

curse_screen = """OUTPUT: //////////////////////////////////////////////////////////////////////
/                                                                            /
/                                                                            /
//////////////////////////////////////////////////////////////////////////////
INPUT:                                                               SPEED:x1
Data              
|     |     |     |     |     |     /     \\     |     |     |     |     |     |
|     |     |     |     |     |     \\     /     |     |     |     |     |     |
                                                                          
Program                                   
                                    /     \\                                   
|     |     |     |     |     |     \\     /     |     |     |     |     |     |
                                                                  
....[LEFT:Decrease Speed]...[RIGHT:Increase Speed]...[DOWN:One Step (on x0)]..."""

if os.getenv("PRINT_BLANK_DATA_TO_ENSURE_ENLARGED_TERMINAL_IN_IDE", default=False):
    for _ in range(16): print(" " * 80); sleep(0.00001);

class Queues:
    def __init__(self):
        self.input = None
        self.shutdown = None
        self.output = None
        self.commands = None


queues = Queues()


def start_curse_queues():
    global queues

    queues.input = Queue()
    queues.shutdown = Queue()
    queues.output = Queue()
    queues.commands = Queue()


def start_curse_engine():
    global queues

    stdscr = curses.initscr()
    curses.noecho()
    curses.curs_set(0)
    stdscr.keypad(True)

    outputwin = stdscr.subwin(14, 80, 0, 0)
    inputwin = stdscr.subwin(2, 80, 14, 0)

    def outputThreadFunc():
        t = time()
        for e, line in enumerate(curse_screen.split("\n")):
            outputwin.addstr(e, 0, line)
        outputwin.move(0, 0)
        while queues.shutdown.empty():
            try:
                if not queues.output.empty():
                    y, x, inp = queues.output.get()
                    if (y, x) != (8, 79):
                        outputwin.addstr(y, x, inp)
            except Empty:
                pass
            if time() - t > 0.05:
                t = time()
                outputwin.refresh()

    def inputThreadFunc():
        inputwin.addstr("-" * 80)
        inputwin.addstr("")
        inputwin.timeout(200)
        while queues.shutdown.empty():
            input_char = inputwin.getch()
            if input_char != -1:
                if 32 <= input_char and 126 >= input_char:
                    queues.input.put(input_char)
                else:
                    if input_char in [curses.KEY_UP, curses.KEY_LEFT, curses.KEY_DOWN, curses.KEY_RIGHT]:
                        queues.commands.put(input_char)

    outputThread = Thread(target=outputThreadFunc)
    inputThread = Thread(target=inputThreadFunc)
    outputThread.start()
    inputThread.start()


class ONABOBFE4P_emulation_using_curse(ONABOBFE4P_emulation_base):
    """More a proof of concept than anything else, this emulator uses curse and can change the speed operations
    proccessed. So you may have no delay (max), a huge delay (x1) or even halt the execution all together (x0)."""
    def __init__(self, program, initial_data=None):

        start_curse_queues()

        self.speeds = [None, 1, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0]
        self.speed_labels = ['x0 ', 'x1  ', 'x2 ', 'x4 ', 'x8 ', 'x16', 'x32', 'x64', 'max']
        self.current_speed = 1

        self.input_queue = queues.input
        self.output_queue = queues.output
        self.shutdown_queue = queues.shutdown
        self.commands_queue = queues.commands
        self.x = 0
        self.y = 1
        self.move_change = True
        self.value_change = True
        self.delay= self.speeds[self.current_speed]

        def print_curse(c):
            self.x += 1
            if self.x == 77:
                self.x = 1
                self.y += 1
                if self.y == 3:
                    self.y = 1
            self.output_queue.put((self.y, self.x, c))

        def input_curse():
            input_char = None
            while input_char is None:
                if not self.input_queue.empty():
                    input_char = chr(self.input_queue.get())
            self.output_queue.put((4, 6, input_char))
            return [input_char]

        def update_curse_screen(self, when, error):
            if when == "END_STEP":

                self.output_queue.put((9, 9, str(self.program_pointer - 1)))
                for e, x in enumerate(range(1, 78, 6)):
                    if (self.program_pointer + e - 6 >= 0) and (self.program_pointer + e - 6 < len(self.program)):
                        self.output_queue.put((11, x, self.program[self.program_pointer + e - 6] + "  "))
                    else:
                        self.output_queue.put((11, x, "XXX"))

                if self.move_change:
                    self.output_queue.put((5, 5, str(self.data_pointer)))
                    for e, x in enumerate(range(1, 78, 6)):
                        if self.data_pointer + e - 6 >= 0 and self.data_pointer + e - 6 < self.max_data:
                            val = self.data[self.data_pointer + e - 6]
                            if 32 <= val and 126 >= val:
                                self.output_queue.put((6, x, "'" + chr(val) + "'"))
                            else:
                                self.output_queue.put((6, x, "   "))
                            self.output_queue.put((7, x, str(val) + "  "))
                        else:
                            self.output_queue.put((6, x, "     "))
                            self.output_queue.put((7, x, "     "))

                elif self.value_change:
                    val = self.data[self.data_pointer]
                    if 32 <= val and 126 >= val:
                        self.output_queue.put((6, 1 + 36, "'" + chr(val) + "'"))
                    else:
                        self.output_queue.put((6, 1 + 36, "   "))
                    self.output_queue.put((7, 1 + 36, str(val) + "  "))

            if when in [">", "<", "-", "+", "[", "]", ".", ",", "END_STEP"]:
                self.move_change = when in [">", "<", "[", "]"]
                self.value_change = when in ["+", "-", ","]

            return True, False

        def finish_curse_when_program_done(self, when, error):
            if when == "DONE":
                sleep(4)
                self.shutdown_queue.put(1)
            return True, False

        super().__init__(" " + program, initial_data, max_data=30000,
                         hooks=[update_curse_screen, finish_curse_when_program_done],
                         io_output=print_curse, io_input=input_curse,
                         max_cell_value=2 ** 8, use_negatives=False,
                         allow_pointer_overflow=False, allow_pointer_underflow=False,
                         allow_data_overflow=False, allow_data_underflow=False)

    def answer_commands(self):
        command_continue = False
        if not self.commands_queue.empty():
            command = self.commands_queue.get()
            change_speed = False
            if command == curses.KEY_RIGHT:
                if self.current_speed + 1 < len(self.speeds):
                    self.current_speed += 1
                    self.delay = self.speeds[self.current_speed]
                    change_speed = True
            if command == curses.KEY_LEFT:
                if self.current_speed > 0:
                    self.current_speed -= 1
                    self.delay = self.speeds[self.current_speed]
                    change_speed = True
            if command == curses.KEY_DOWN and self.speeds[self.current_speed] is None:
                command_continue = True
            if change_speed:
                self.output_queue.put((4, 75, self.speed_labels[self.current_speed]))
        return command_continue

    def run(self):
        try:
            start_curse_engine()
            super()._run_with_step(self._step)
        except Exception as e:
            self.shutdown_queue.put(1)
            raise e

    def _step(self):
        command_continue = self.answer_commands()
        if self.delay is not None or command_continue:
            if self.delay is not None:
                sleep(self.delay)
            do_continue = super()._step()
        else:
            do_continue = True
            sleep(1)
        return do_continue


if __name__ == "__main__":
    hello_world = ">++++++++[<+++++++++>-]<.>++++[<+++++++>-]<+.+++++++..+++.>>++++++[<+++++++>-]<++.------------.>++++++[<+++++++++>-]<+.<.+++.------.--------.>>>++++[<++++++++>-]<+."
    ONABOBFE4P_emulation_using_curse(hello_world, None).run()
