# Oh No, Another Bunch Of Brain F*ck Emulators, For Python

## Introduction

_TL;DR This is a project to help you interpret/emulate BrianF*ck programs in Python. You can either use the interpreters
/emulators that are already bundled with it or easily create custom ones that follow the exact specifications you need._

Since BF was designed to be an easy2compile language (not really caring if it was actually useful), the job 
of creating a personal interpreter can be pretty straight-forward. Originally called _"Oh No Another Tiny BF Emulator"_, 
I created this project to do some debugging in BF, as using a custom interpreter allowed me to know 
where to look. 

However, there was potential for more. The hooks I was using for debugging could be abstracted, creating a 
more customizable program. Following that same logic, certain behaviours could be made controllable by initialization 
arguments, allowing the user to create a huge number of different BF interpreters/machines. This is important since 
[BF is not a thoroughly defined language](https://en.wikipedia.org/wiki/Brainfuck#Portability_issues), and issues like 
cell-size, computer number format (8-bits/16-bits, signed/unsigned, etc) or pointer behaviour after going beyond the 
threshold are not defined and can be decided by each programmer.

As such, ONABOBFE4P can be though as a Multi-specification BrainF*ck interpreter/emulator with hooks to enable 
customized behaviour and easy debugging.

## How to run

To run a bundled emulator, simply use the CLI client. You can either run it in interactive mode or clarify all the variables via the inline mode.

For inline you will need to add an emulator name and either a program file or a sting (with the whole program). 

Examples:

    ./ONABOBFE4P_CLI.py interactive
    ./ONABOBFE4P_CLI.py inline --e vainilla --path program.bf
    ./ONABOBFE4P_CLI.py inline --e stateful-print --prog "s>++++++++[<+++++++++>-]<.>++++[<+++++++>-]<+.+++++++..+++.>>++++++[<+++++++>-]<++.------------.>++++++[<+++++++++>-]<+.<.+++.------.--------.>>>++++[<++++++++>-]<+."
    

## How to use a customized Emulator

You just need to import the ONABOBFE4P_emulation_base and create a subclass, for example:

    class FIRST_EMULATOR(ONABOBFE4P_emulation_base):
  
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

I suggest you check the folder ``Emulators/Bundled``, where there are a handful of examples already created. In case you 
add a new file, you will also need to modify the ``ONABOBFE4P_CLI.py`` to add it to the emulators by adding it to the 
dictionary with some name of your choice.


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


## Simple BF Standard Specification

Since there are no technical specification for many of the BF language features, I decided to make an "Standard" specification of my own. Most of the "examples" contained in this project use it as a base. The idea was to keep it simple as possible and make something that hardware could trivialy emulate:

* The numbers are represented as positive integers of 8 bits. 

* There is no overflow or underflow. If trying to add beyond the max number allowed or subtracting beyond zero, an error will rise.

* The size of memory is 30000 (value used by  Urban Müller) by default.

* Trying to move the data pointer below zero or above "max_data" will result in an error.


## Wait a second, if this is mostly a customizable Interpreter, why is it called Emulator?

That's a fair question, since an Emulator and an Interpreter are technically not the same thing. (despite the fact
that some emulators are designed as interpreters). In my personal opinion, give the memory constrains imposed by BF, it 
does make sense to think of it as a virtual computer instead of just a language specification. 
[BF machines do exists in the wild](https://hackaday.io/project/18599-brainfuckpc-relay-computer), as well as 
[different hardware specifications](https://github.com/asumagic/tinydumbcpu).  

Moreover, the existence of an emulator "with quantum" is to allow certain degree of "hardware emulation", by allowing 
the user to add an artificial "mechanical delay" to each operation on its own. That way, certain BF machines could be 
emulated.

However, feel free to call this project an Interpreter, since it's a correct definition for it.
