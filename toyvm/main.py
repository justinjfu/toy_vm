#!/usr/bin/python
import argparse
from assembler import parse_with_preprocess
from runtime import VMRuntime
from ctrans.translator import compilecode


def parse_args():
    parser = argparse.ArgumentParser(description='Executes an assembly program')
    parser.add_argument('asm_file', type=str, help='Filename of program to execute')
    parser.add_argument('--debug', '-d', action='store_true', default=False, help='Print debug messages')
    parser.add_argument('--compile', '-c',type=str, help='Compile to machine code rather than execute')
    parser.add_argument('--memory', '-m', type=int, default=128, help='Size of memory (in ints)')
    parser.add_argument('--stack', '-s', type=int, default=4096, help='Max stack size (in ints). Currently unused by python')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    program = parse_with_preprocess(args.asm_file)

    if args.compile:
        compilecode(program, args.compile, stack_size=args.stack, mem_size=args.memory) 
    else:
        runtime = VMRuntime(program, args.memory, args.stack)
        runtime.debug = args.debug
        runtime.spawn_master()
        runtime.run()

    if args.debug:
        print 'Memory: %r' % runtime.memory

if __name__ == "__main__":
    main()
