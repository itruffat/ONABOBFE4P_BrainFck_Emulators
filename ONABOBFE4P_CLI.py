import argparse as AP
import glob, os

from Emulators.Bundled.VainillaEmulator import ONABOBFE4P_emulation_plain
from Emulators.Bundled.StatefulEmulator import ONABOBFE4P_emulation_with_statefull_print
from Emulators.Bundled.QuantumEmulator import ONABOBFE4P_emulation_with_quantum

emulators = {
    'stateful-print':ONABOBFE4P_emulation_with_statefull_print,
    'vainilla':ONABOBFE4P_emulation_plain,
    'quantum':ONABOBFE4P_emulation_with_quantum
}

argparser = AP.ArgumentParser(description='CLI to run OhNoAnotherBrainFckEmulator4Python')


subparsers = argparser.add_subparsers(help='sub-command help')

subparsers.add_parser('interactive', help='a help')
argparser1 = subparsers.add_parser('inline', help='a help')
argparser1.add_argument('--e',
                       choices=emulators.keys(),
                       help='Pick an emulator profile',
                       required = True
                       )

program_group = argparser1.add_mutually_exclusive_group(required=True)

program_group.add_argument('--path',
                       metavar='path2program',
                       type=open,
                       help='Path to program to run'
                        )

program_group.add_argument('--prog',
                       metavar='stringProgram',
                       type=str,
                       help='Program to run'
                        )

args = argparser.parse_args()

if 'e' not in args:

    keys = list(emulators.keys())
    sorted(keys)
    if len(keys) < 1:
        print("That's weird, no emulators were found. Please check.")
        exit(1)
    print("Please choice an emulator")
    for e, emulator in enumerate(keys):
            print(f'{e}. {emulator}')
    print("x. Exit")
    i = input()
    not_valid_answer = "Answer was not valid. Exiting"
    if i not in [*map(str, range(len(keys))), "x"]:
        print(not_valid_answer)
        exit(1)
    if i == "x":
        print("bye")
        exit(0)
    args.e = keys[int(i)]
    print(args.e)
    print("Do you want to [w]rite the program or [l]oad a file?")
    i = input()
    if i not in ["w","l"]:
        print(not_valid_answer)
        exit(1)
    if i == "l":
        os.chdir(".")
        files = glob.glob("*.bf")
        if len(files) < 1:
            print("No .bf files found on this folder, please add them.")
            exit(1)
        for n, file in enumerate(files):
            print(f'{n}. {file}')
        i = input()
        if i not in map(str, range(len(files))):
            print(not_valid_answer)
            exit(1)
        args.prog = None
        args.path = open(files[int(i)],"r")
    elif i == "w":
        print("Please write the program")
        args.prog = input()
        args.path = None

if 'e' in args:
    program = args.prog if args.prog is not None else args.path.read()
    emulators[args.e](program).run()