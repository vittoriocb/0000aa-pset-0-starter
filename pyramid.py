#!/usr/bin/env python3
"""Print a pyramid to the terminal

A pyramid of height 3 would look like:

--=--
-===-
=====

"""

from argparse import ArgumentParser, RawDescriptionHelpFormatter


def calculate_line(line_number):
    """Returns the number of '=' on a line
    The number of '=' in the line can be defined by the function
    n = (line_number - 1)*2 + 1

    :param int line_number: 1-based line number in the pyramid
    :rtype: int
    """

    n = (line_number - 1) * 2 + 1
    return n


def print_pyramid(rows):
    """Print a pyramid of a given height

    :param int rows: total height
    """

    try:
        rows = int(rows)
        # This would be the maximum width of the triangle / size of the base.
        # All lines should have this total width in number of characters
        n_max = calculate_line(rows)

        for i in range(1, rows + 1):
            num = calculate_line(i)
            # A simple way to fill empty spaces in a line with our desired character
            print(("=" * num).center(n_max, "-"))

    except ValueError as val_error:
        raise ValueError("--rows must be an integer") from val_error


def main():
    """Main entry point of the program"""
    parser = ArgumentParser(
        description=__doc__, formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument("-r", "--rows", default=10, help="Number of rows")

    args = parser.parse_args()
    print_pyramid(args.rows)


if __name__ == "__main__":
    main()
