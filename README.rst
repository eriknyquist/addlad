PainStruck - an esoteric programming language
---------------------------------------------

``PainStruck`` is an esoteric programming language inspired partially by `Brainf**k <https://en.wikipedia.org/wiki/Brainfuck>`_
and partially by Chris Domas' `movfuscator <https://github.com/xoreaxeaxeax/movfuscator>`_

``PainStruck`` programs operate on a "memory tape", a fixed-size array of 8-bit unsigned integers.
There is only a single operation available in ``PainStruck``, which reads a value from one array
index (the source index), and adds it to the value stored in another array index (the destination
index). A single operation consists of an integer (the destination array index, where the
result will go), followed by a comma, followed by another integer (the source array index),
and finally a semicolon:

.. code::

    6, 7;   # Read from array index 7, and add to value stored in index 6
    6, 8;   # Read from array index 8, and add to value stored in index 6

Enclosing an array index with square brackets ``[]`` will cause the value at that
array index to be used as the array index (i.e. a pointer to another array index):

.. code::

    6, [7]; # Read from array index stored at array index 7, and add to value stored in index 6

Practical details
=================

In order to make "normal" programming activities possible with only a single operation,
4 specific negative array indices (-1 through -4) are reserved for special purposes, and are
referred to as "registers":

* **array index -1: Output register** Using index -1 as the destination index will write
  the value at the source index to stdout. **Using index -1 as the source index will add
  1 to the value stored in the destination index. This is the only way you can change
  any initial value in the array from 0 to 1, and most programs will start by adding array
  index -1 to some other array index**.

* **array index -2: Input register** Using index -2 as the source index will read
  1 character from stdin, and then write the read value to the destination index.
  Using index -2 as the destination index will have no effect.

* **array index -3: Instruction pointer increment register** Using index -3 as the
  destination index will add the value at the source index to the current instruction
  pointer value. If the value at the source index is zero, then the instruction pointer
  will not be changed and execution will continue normally. Using index -3 as the source
  index will result in no change to the destination index.

* **array index -4: Instruction pointer decrement register** Using index -4 as the
  destination index will subtract the value at the source index from the current
  instruction pointer value. If the value at the source index is zero, then the
  instruction pointer will not be changed and execution will continue normally. Using
  index -4 as the source index will result in no change to the destination index.

NOTE: None of the register can be used with pointer syntax (e.g. ``[-1]``), and this
will be a parsing failure.

In addition to the registers, there are some extra details needed in order to write
working ``PainStruck`` programs:

* Array index 262 will always contain a value of 1 on program start, and all other
  array indices will contain a value of 0.

* All array values (including registers) are 8-bit unsigned integers, so values are
  fixed between 0-255. Integer overflow/underflow will wrap around.

* Using the same array index for the source and destination is allowed, and will
  behave as expected, i.e. the value stored at the array index will be doubled

* Instruction pointer increments or decrements are allowed to overflow/underflow.
  They will wrap around to the first/last instruction in this case.

* Default array size is 100k elements

* All whitespace is ignored. Single-line comments are available with the ``#`` character.

"Hello world" in PainStruck
---------------------------

.. code::

	5,4;    # Index 4 contains '1', copy it to index 5
	5,5;    # Put '2' in index 5, for arithmetic later
	6,5;
	6,6;    # Put '4' in index 6, for arithmetic later
	7,6;
	7,7;    # Put '8' in index 7, for arithmetic later
	25,7;   # Index 25, space character
	25,25;
	25,25;
	20,25;  # Index 20, first character 'H'
	20,20;
	20,7;
	30,20;  # Index 30,  last character 'd'
	30,7;
	30,7;
	30,7;
	30,6;
	21,30;  # Index 21, 'e' character
	21,4;
	22,21;  # Index 22, first 'l' character
	22,6;
	22,4;
	22,4;
	22,4;
	23,22;  # Index 23, second 'l' character
	29,23;  # Index 29, last 'l' character
	24,29;  # Index 24, first 'o' character
	24,5;
	24,4;
	27,24;  # Index 27, last 'o' character
	28,27;  # Index 28, 'r' character
	28,5;
	28,4;
	26,28;  # Index 26, 'w' character
	26,6;
	26,4;
	31,7;   # Index 31, newline character
	31,5;
	0,20;   # Print 'H'
	0,21;   # Print 'e'
	0,22;   # Print 'l'
	0,23;   # Print 'l'
	0,24;   # Print 'o'
	0,25;   # Print ' '
	0,26;   # Print 'w'
	0,27;   # Print 'o'
	0,28;   # Print 'r'
	0,29;   # Print 'l'
	0,30;   # Print 'd'
	0,31;   # Print '\n'
