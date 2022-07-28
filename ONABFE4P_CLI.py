import argparse as AP
from Emulators.VainillaEmulator import ONABFE4P_emulation_plain
from Emulators.HookableEmulator import ONABFE4P_emulation_with_statefull_print

emulators = {
    'stateful':ONABFE4P_emulation_with_statefull_print,
    'vainilla':ONABFE4P_emulation_plain
}

argparser = AP.ArgumentParser(description='CLI to run OhNoAnotherBrainFckEmulator4Python')

argparser.add_argument('--e',
                       choices=emulators.keys(),
                       help='Pick an emulator profile',
                       required = True
                       )

program_group = argparser.add_mutually_exclusive_group(required=True)

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

program = args.prog if args.prog is not None else args.path.read()

emulators[args.e](program).run()