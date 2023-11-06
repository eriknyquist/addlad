import sys
import os


DEFAULT_TAPE_SIZE = 300000

def parse(filename, tape_size=DEFAULT_TAPE_SIZE):
    ret = []

    # Strip out comments
    with open(filename, 'r') as fh:
        buf = ""
        in_comment = False
        line = 1
        column = 0

        while True:
            char = fh.read(1)
            column += 1

            if not char:
                break


            if char == "\n":
                in_comment = False
                column = 0
                line += 1

            elif char == "#":
                in_comment = True

            elif in_comment:
                continue

            elif char.isspace():
                continue

            elif char == ";":
                fields = buf.split(",")
                if len(fields) != 2:
                    raise ValueError(f"Invalid operation '{buf}' in {filename} (line {line}, column {column})")

                try:
                    dest = int(fields[0])
                except ValueError:
                    raise ValueError(f"Invalid array index '{fields[0]}' in {filename} (line {line}, column {column})")

                try:
                    src = int(fields[1])
                except ValueError:
                    raise ValueError(f"Invalid array index '{fields[1]}' in {filename} (line {line}, column {column})")

                if (dest < 0) or (dest > tape_size):
                    raise ValueError(f"Invalid array index '{dest}' in {filename} (line {line}, column {column})")
                    
                if (src < 0) or (src > tape_size):
                    raise ValueError(f"Invalid array index '{src}' in {filename} (line {line}, column {column})")
                    
                buf = ""
                ret.append([dest, src])

            else:
                if char.isdigit() or (char in ",;"):
                    buf += char
                else:
                    raise ValueError(f"Invalid character '{char}' in {filename} (line {line}, column {column})")

    return ret

def execute(ops, tape_size=DEFAULT_TAPE_SIZE):
    tape = bytearray(tape_size)
    tape[4] = 1
    index = 0

    while index < len(ops):
        dest = ops[index][0]
        src = ops[index][1]

        # First, obtain value from src
        if src == 1:
            src_val = ord(os.read(0, 1))
        else:
            src_val = tape[src]

        # Now, handle writing to dest
        if dest == 0:
            # Print contents of cell 'src' to stdout
            sys.stdout.write(chr(src_val))
            sys.stdout.flush()
            index += 1
        elif dest == 2:
            # increment instruction pointer by value at 'src'
            index = (index + src_val) % len(ops)
        elif dest == 3:
            # decrement instruction pointer by value at 'src'
            index -= src_val
            if index < 0:
                index = len(ops) + index
        else:
            tape[dest] = (tape[dest] + src_val) % 256
            index += 1

ops = parse(sys.argv[1])
for dest, src in ops:
    print(f"move {src} to {dest}")

execute(ops)

