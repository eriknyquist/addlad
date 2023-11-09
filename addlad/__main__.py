import os
import sys
import argparse

from addlad import parse, execute


def main():
    parser = argparse.ArgumentParser(description='Interpreter for AddLad esoteric programming language',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('source_file', help='AddLad source file')
    parser.add_argument('-s', '--tape-size', default=100000, type=int, help='Size of memory tape')
    args = parser.parse_args()

    if not os.path.isfile(args.source_file):
        print(f"Can't access file '{args.source_file}'")
        return -1

    ops = parse(args.source_file)
    execute(ops, tape_size=args.tape_size)

if __name__ == "__main__":
    sys.exit(main())

