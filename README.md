# Oh No Another Brain F*ck Emulator (For Python)

## Introduction

As the name implies, this is just another BrianF*ck emulator done in Python. BF was originally designed as an easy language to compile language (not really caring if it was actually useful), which also made the job of creating a personal emulator for it almost trivial. Originally created as _"Oh No Another Tiny BF Emulator"_, I created this project because I wanted to do some experiments in BF, and using a custome emulator allowed me to start debuging fast. 

However, the hooks I was using for debbuging could be abstracted, creating a more customizable code. Following that same logic, certain behaviours could be made controllable by initialization arguments, allowing the user to create a huge number of different BF machines. This is important since [BF is not a thoroughly defined language](https://en.wikipedia.org/wiki/Brainfuck#Portability_issues), and issues like cell-size, computer number format (8-bits/16-bits, signed/unsigned, etc), pointer behaviour after going beyond the treshold are not defined and can be decided by the user.

As such, ONABFE4P is a library that allows you to create a BF emulator that follows the specifications you need.

## Customizable args

When creating a new BF Emulation, the following parameters are used:

     * program: The BF program to be run, it must be an string.
     * initial_data: A way to initialize the array for testing. It's not compulsory and if left as "None" it will be
                     automatically filled with zeros. It must always have a length equal to max_data.
     * max_data: The size of the data stack.
     * hooks: Functions that are called during certain parts of the execution. Sublcasses can have their own hooks to
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

## How to use

You just need to import the ONABFE4P_emulation_base and create a subclass, for example

    class FIRST_EMULATOR(ONABFE4P_emulation_base):
  
        def __init__(self, program):
            def print_default(x): print(x, end='')

            def input_default(): return input()

            super().__init__(program, initial_data=None, max_data=30000, hooks=[],
                         io_output=print_default, io_input=input_default,
                         max_cell_value=2**8, use_negatives=False,
                         allow_pointer_overflow=False, allow_pointer_underflow=False,
                         allow_data_overflow=False, allow_data_underflow=False)
   
    hello_world = ">++++++++[<+++++++++>-]<.>++++[<+++++++>-]<+.+++++++..+++.>>++++++[<+++++++>-]<++.------------.>++++++[<+++++++++>-]<+.<.+++.------.--------.>>>++++[<++++++++>-]<+."

    FIRST_EMULATOR(hello_world, None).run()

In the folder ``Emulators`` there will be a handful of examples already created. You can use one of those, or copy and 
customize it to create your own!

## Simple BF Standard Specification

Since there are no technical specification for many of the BF language features, I decided to make an "Standard" specification of my own. Most of the "examples" contained in this project use it as a base. The idea was to keep it simple as possible and make something that hardware could trivialy emulate:

* The numbers are represented as positive integers of 8 bits. 

* There is no overflow or underflow. If trying to add beyond the max number allowed or subtracting beyond zero, an error will rise.

* The size of memory is 30000 (value used by  Urban Müller) by default.

* Trying to move the data pointer below zero or above "max_data" will result in an error.

