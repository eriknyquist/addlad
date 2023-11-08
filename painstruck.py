import sys
import os


DEFAULT_TAPE_SIZE = 100000
MIN_TAPE_SIZE = 262

def _parse_array_index(tape_size, field, line, column):
    is_pointer = False

    if field.startswith('[') and field.endswith(']'):
        is_pointer = True
        field = field.strip('[]')

    try:
        ret = int(field)
    except ValueError:
        raise ValueError(f"Invalid array index '{fields[0]}' in {filename} (line {line}, column {column})")

    if (ret < -4) or (ret > tape_size):
        raise ValueError(f"Invalid array index '{dest}' in {filename} (line {line}, column {column})")

    if (ret < 0) and is_pointer:
        raise ValueError(f"Registers cannot be used with pointer syntax: '{field}' (line {line}, column {column})")

    return ret, is_pointer

def parse(filename, tape_size=DEFAULT_TAPE_SIZE):
    if tape_size < MIN_TAPE_SIZE:
        raise ValueError(f"Tape size must be at least {MIN_TAPE_SIZE} bytes")

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

                dest, dest_is_ptr = _parse_array_index(tape_size, fields[0].strip(), line, column)
                src, src_is_ptr = _parse_array_index(tape_size, fields[1].strip(), line, column)

                buf = ""
                ret.append([dest, dest_is_ptr, src, src_is_ptr])

            else:
                if char.isdigit() or (char in "[]-,;"):
                    buf += char
                else:
                    raise ValueError(f"Invalid character '{char}' in {filename} (line {line}, column {column})")

    return ret

def execute(ops, tape_size=DEFAULT_TAPE_SIZE):
    if tape_size < MIN_TAPE_SIZE:
        raise ValueError(f"Tape size must be at least {MIN_TAPE_SIZE} bytes")

    tape = bytearray(tape_size + 4)
    tape[-1] = 1
    index = 0

    while index < len(ops):
        dest = ops[index][0]
        dest_is_ptr = ops[index][1]
        src = ops[index][2]
        src_is_ptr = ops[index][3]

        # First, obtain value from src
        if src == -2:
            src_val = ord(os.read(0, 1))
        elif src_is_ptr: # Read pointer
            src_val = tape[tape[src]]
        else:
            src_val = tape[src]

        # Now, handle writing to dest
        if dest == -1: # Write
            sys.stdout.write(chr(src_val))
            sys.stdout.flush()
        elif dest == -3: # Increment instruction pointer
            if src_val > 0:
                index = (index + src_val) % len(ops)
                continue # Skip instruction pointer += 1
        elif dest == -4: # Decrement instruction pointer
            if src_val > 0:
                index -= src_val
                if index < 0:
                    index = len(ops) + index

                continue # Skip instruction pointer += 1
        elif dest_is_ptr: # Write pointer
            tape[tape[dest]] = (tape[tape[dest]] + src_val) % 256
        else:
            tape[dest] = (tape[dest] + src_val) % 256

        index += 1

ops = parse(sys.argv[1])
execute(ops)

