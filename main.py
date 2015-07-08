import argparse
from assembler import parse_file
from runtime import VMRuntime


def parse_args():
    parser = argparse.ArgumentParser(description='Executes an assembly program')
    parser.add_argument('asm_file', type=str, help='Filename of program to execute')
    parser.add_argument('--debug', '-d', action='store_true', default=False, help='Print debug messages')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    program = parse_file(args.asm_file)

    runtime = VMRuntime(program)
    runtime.debug = args.debug

    runtime.spawn_master()
    runtime.run()

if __name__ == "__main__":
    main()
