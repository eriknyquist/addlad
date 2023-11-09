AddLad - an esoteric programming language
-----------------------------------------

``AddLad`` is an esoteric programming language inspired partially by `Brainf**k <https://en.wikipedia.org/wiki/Brainfuck>`_
and partially by Chris Domas' `movfuscator <https://github.com/xoreaxeaxeax/movfuscator>`_.

``AddLad`` programs operate on a "memory tape", a fixed-size array of 8-bit unsigned integers.
There is only a single operation available in ``AddLad``, which reads a value from one array
index (the source index), and adds it to the value stored in another array index (the destination
index). That's It. A single operation consists of an integer (the destination array index, where the
result will go), followed by a comma, followed by another integer (the source array index),
and finally a semicolon:

.. code::

    6, 7;   # Read from array index 7, and add to value stored in index 6
    6, 8;   # Read from array index 8, and add to value stored in index 6

Enclosing an array index with square brackets ``[]`` will cause the value at that
array index to be used as the array index (i.e. a pointer to another array index):

.. code::

    6, [7]; # Read from array index stored at array index 7, and add to value stored in index 6

Registers
=========

In order to facilitate some of the features that programmers are accustomed to
(specifically input, output, modifying the instruction pointer, and non-zero values), 4
specific negative array indices (-1 through -4) are reserved for special purposes,
and are referred to as "registers":

* **array index -1: Output register** Using index -1 as the destination index will write
  the value at the source index to stdout. **Using index -1 as the source index will add
  1 to the value stored in the destination index. This is the only way you can change
  any initial value in the array from 0 to 1, and most programs will start by adding array
  index -1 to some other array index**.

* **array index -2: Input register** Using index -2 as the source index will read
  1 character from stdin, and then add the read value to the value stored at the destination
  index. Using index -2 as the destination index will result in no change to the value at the
  source index.

* **array index -3: Instruction pointer increment register** Using index -3 as the
  destination index will add the value at the source index to the current instruction
  pointer value. If the value at the source index is zero, then the instruction pointer
  will not be changed and execution will continue normally. Using index -3 as the source
  index will result in no change to value at the destination index.

* **array index -4: Instruction pointer decrement register** Using index -4 as the
  destination index will subtract the value at the source index from the current
  instruction pointer value. If the value at the source index is zero, then the
  instruction pointer will not be changed and execution will continue normally. Using
  index -4 as the source index will result in no change to the value at the destination index.

NOTE: None of the registers can be used with pointer syntax (e.g. ``[-1]``), and this
will be a parsing failure.

Additional technical specifications
===================================

* All array values (including registers) are 8-bit unsigned integers, so values are
  fixed between 0-255. Integer overflow/underflow will wrap around.

* Using the same array index for the source and destination is allowed, and will
  cause the value stored at the array index to be doubled.

* Instruction pointer increments or decrements are allowed to overflow/underflow.
  They will wrap around to the first/last instruction in this case.

* Default array size is 100k elements

* All whitespace is ignored. Single-line comments are available with the ``#`` character.

"Hello world" in AddLad
------------------------

.. code::

    263,-1;     # Add 1 to index 263
    263,263;    # Put '2' in index 263, for arithmetic later
    264,263;
    264,264;    # Put '4' in index 264, for arithmetic later
    265,264;
    265,265;    # Put '8' in index 265, for arithmetic later
    25,265;     # Index 25, space character
    25,25;
    25,25;
    20,25;      # Index 20, first character 'H'
    20,20;
    20,265;
    30,20;      # Index 30,  last character 'd'
    30,265;
    30,265;
    30,265;
    30,264;
    21,30;      # Index 21, 'e' character
    21,-1;
    22,21;      # Index 22, first 'l' character
    22,264;
    22,263;
    22,-1;
    23,22;      # Index 23, second 'l' character
    29,23;      # Index 29, last 'l' character
    24,29;      # Index 24, first 'o' character
    24,263;
    24,-1;
    27,24;      # Index 27, last 'o' character
    28,27;      # Index 28, 'r' character
    28,263;
    28,-1;
    26,28;      # Index 26, 'w' character
    26,264;
    26,-1;
    31,265;     # Index 31, newline character
    31,263;
    -1,20;      # Print 'H'
    -1,21;      # Print 'e'
    -1,22;      # Print 'l'
    -1,23;      # Print 'l'
    -1,24;      # Print 'o'
    -1,25;      # Print ' '
    -1,26;      # Print 'w'
    -1,27;      # Print 'o'
    -1,28;      # Print 'r'
    -1,29;      # Print 'l'
    -1,30;      # Print 'd'
    -1,31;      # Print '\n'


How do I write an "if" statement with AddLad?
---------------------------------------------

It may seem like ``AddLad`` isn't capable of constructs like this:

.. code:: c

    if ((value >= LOWER_BOUND) && (value <= UPPER_BOUND))
    {
        // Some conditional code
    }

But if we take some inspiration from Stephen Dolan's
`"mov is Turing-complete" <https://drwho.virtadpt.net/files/mov.pdf>`_ paper,
and Chris Domas' `MovFuscator <https://github.com/xoreaxeaxeax/movfuscator>`_ project, we
can do some interesting things.

This section shows how to create an ``AddLad`` program that reads 1 byte from
stdin, and prints ``uppercase`` if the read byte is an ASCII uppercase letter,
and prints ``lowercase`` otherwise. The full example program is available
`in the Github repo <https://github.com/eriknyquist/addlad/blob/master/examples/condition.ps>`_

1. Fill array indices 65 through 90 (ASCII 'A' through 'Z') with a value of 1:

   .. code::

        65,-1;
        66,-1;
        67,-1;
        68,-1;
        69,-1;
        70,-1;
        71,-1;
        72,-1;
        73,-1;
        74,-1;
        75,-1;
        76,-1;
        77,-1;
        78,-1;
        79,-1;
        80,-1;
        81,-1;
        82,-1;
        83,-1;
        84,-1;
        85,-1;
        86,-1;
        87,-1;
        88,-1;
        89,-1;
        90,-1;

   It's important that all other array indices in the 0-255 range remain at their
   initial default value of 0. So array indices 0-64 should hold a value of 0, array
   indices 65-90 should hold a value of 1, and finally array indices 91-255 should hold
   a value of 0. You'll see why in the following steps.

2. Read 1 byte from stdin:

   .. code::

       260,-2;

3. Interpret the byte read from stdin as an array index, and read the value
   stored at that array index:

   .. code::

       261,[260];

   If the read value is 1, then we know that the byte read from stdin is an uppercase
   letter, since it's within the range of array indices that we set to a value of 1
   in step #1.

   If the read value is 0, then we know that the byte read from stdin is *not* an
   uppercase letter, since it's outside the range of array indices that we set to a value
   of 1 in step #1, and those array indices will still be at their default value of 0.

4. You can now use the value of "0" or "1" obatined in step #3 to (for example) switch
   between different array indices which contain different instruction pointer decrement
   values. This is how the ``examples/condition.ps`` program decides which characters to
   print.
