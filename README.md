# OhNoAnotherTinyBrainF*ckEmulator

As the name implies, this is another BrianF*ck emulator done in python. I wanted to do some experiments in BF, and since 
BF is so simple, I wanted to use an emulator of my own for debugging.

## BF machine specification

There is no technical specification for many BF language features and a lot of the things it does, meaning it can be freely interpreted. Here are the interpretations I made:

* There is no overflow or underflow. If trying to add beyond the max number allowe or subtracting beyond zero, an error will rise.

* The numbers are positive integers of 16 bits. 

* The size of memory can be modified as a parameter (max_data), but it's 3000 by default.

* Trying to move the data pointer below zero or above "max_data" will result in an error.

## To take into consideration when running a new emulator

To emulation takes a couple of paramenters:

* initial_data: How the BF stack is initalized. Technically speaking, data should always be initialized as 0 and the program itself should modify these values. However, when testing new things it is useful to be able to skip all that.

* Peep: It can be used to see data at the start of a "frame" (before anything is modified)

* Intercept: Exactly the same as peep, but every input can be replaced for something else, specially useful when you want to modify some behaviour after certain moment.

* print_f: How things are printed. This is here in case one wants to customize the way the output is returned.

* input_f: Same as the one above, this let's you customize the way information is introduced. 

## SetUp Examples

For the moment I have a basic setup that allows you to print the memory in specific moments, prints all the output together and aborts when the input is 7. (this was done following ASCII ENCODING) I might add more in the future.
