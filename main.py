import argparse
from assembler import parse_with_preprocess
from runtime import VMRuntime


def parse_args():
    parser = argparse.ArgumentParser(description='Executes an assembly program')
    parser.add_argument('asm_file', type=str, help='Filename of program to execute')
    parser.add_argument('--debug', '-d', action='store_true', default=False, help='Print debug messages')
    parser.add_argument('--memory', '-m', type=int, default=128, help='Size of memory (in ints)')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    program = parse_with_preprocess(args.asm_file)

    runtime = VMRuntime(program, args.memory)
    runtime.debug = args.debug

    runtime.spawn_master()
    runtime.run()

    if args.debug:
        print 'Memory: %r' % runtime.memory

if __name__ == "__main__":
    main()
