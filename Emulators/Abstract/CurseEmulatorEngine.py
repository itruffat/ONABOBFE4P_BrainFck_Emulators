import curses
import os
from threading import Thread
from time import sleep, time
from queue import Queue, Empty

if os.getenv("PRINT_BLANK_DATA_TO_ENSURE_ENLARGED_TERMINAL_IN_IDE", default=False):
    for _ in range(10): print(" " * 80); sleep(0.00001);

class Queues():
    def __init__(self):
        self.input = None
        self.shutdown = None
        self.output = None

queues = Queues()

def start_curse_queues():
    global queues

    queues.input = Queue()
    queues.shutdown = Queue()
    queues.output = Queue()

def start_curse_engine():
    global queues

    stdscr = curses.initscr()
    curses.noecho()
    curses.curs_set(0)
    stdscr.keypad(True)

    upperwin = stdscr.subwin(9, 80, 0, 0)
    lowerwin = stdscr.subwin(2, 80, 9, 0)

    def outputThreadFunc():
        y = 0
        x = 0
        t = time()
        while queues.shutdown.empty():
            try:
                if not queues.output.empty():
                    inp = queues.output.get()
                    if (y, x) == (8, 79):
                        y,x = 0,0
                    upperwin.addstr(y, x, inp)
                    if x == 79:
                        y = (y + 1)%9
                    x = (x+1) % 80
            except Empty:
                pass
            if time() - t > 0.05:
                t = time()
                upperwin.refresh()


    def inputThreadFunc():
        lowerwin.addstr("-"*80)
        lowerwin.addstr("")
        lowerwin.timeout(200)
        while queues.shutdown.empty():
            a = lowerwin.getch()
            if a != -1:
                queues.input.put(a)

    outputThread = Thread(target=outputThreadFunc)
    inputThread = Thread(target=inputThreadFunc)
    outputThread.start()
    inputThread.start()