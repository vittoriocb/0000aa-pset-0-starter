#!/usr/bin/env python3

"""
The original fibonacci function calculates the same f(n) many times. A first gain
in performance would be to store previously calculated numbers in memory, in
order to access those instead of calculating again. Then the fibonacci
recursive function could be left as is and it would work much faster,
but would soon run into a problemwith recursion depth with bigger
numbers (e.g. n=100000). In order to fix the latter, I iterate from 0 to n
calculating and storing the fibonacci number, this way the maximum recursion
depth is kept at a maximum of 1. Further optimizing, we only need to store
the last 2 numbers in the case of fibonacci (and the last n number
when generalizing), doing this saves time and memory.
"""

import time


def optimized_calculate_seq(i, n, initial):
    """Calculates a sequence of numbers where the ith number is the sum of the
    previous n numbers in the sequence, with the first n numbers defined
    arbitrarily.

    :param int i: position of number to calculate
    :param int n: amount of previous numbers to sum at ith position
    :param list(int) initial: arbitrary intial sequence of numbers
    :rtype: int
    """
    if i < 0:
        raise ValueError("Only positive numbers allowed")
    if n > len(initial):
        raise ValueError("n must not be greater than the initial number of elements")

    # If i is in the initial list of numbers then there is no need to calculate it
    if i < len(initial):
        return initial[i]

    last_calc = initial.copy()
    for _ in range(len(last_calc), i + 1):
        calc = sum_sequence(n, last_calc)
        last_calc.append(calc)
        last_calc.pop(
            0
        )  # Keeps list small by removing first element, which is not needed anymore

    result = last_calc[-1]

    return result


def sum_sequence(n, sequence):
    """Returns the sum of the last n numbers of a list

    :param int n: numbers to sum starting at -1 position
    :param list(int) sequence: list of numbers
    :rtype: int
    """
    calc = 0
    for i in range(1, n + 1):
        calc += sequence[-i]
    return calc


def optimized_fibonacci(i):
    """Calculates optimized_calculate_seq for a special case where n=2
    with the first numbers (0, 1)

    :param int i: position of number to calculate
    :rtype: int
    """
    return optimized_calculate_seq(i, n=2, initial=[0, 1])


def last_8(some_int):
    """Return the last 8 digits of an int

    :param int some_int: the number
    :rtype: int
    """

    return int(str(some_int)[-8:])


# pylint: disable=too-few-public-methods
class SummableSequence:
    """A sequence where the ith number is the sum of the last n numbers,
    with an arbitrary defined initial sequence
    """

    def __init__(self, *initial):
        self.__initial = list(initial)
        self.__n = len(self.__initial)

    def __call__(self, i):
        return optimized_calculate_seq(i, n=self.__n, initial=self.__initial)


def main():
    """Main entry point of the program"""
    start = time.perf_counter()
    print("f(100000)[-8:]", last_8(optimized_fibonacci(100000)))
    stop = time.perf_counter() - start
    print("Time elapsed (s)", stop)

    start = time.perf_counter()
    new_seq = SummableSequence(5, 7, 11)
    print("new_seq(100000)[-8:]:", last_8(new_seq(100000)))
    stop = time.perf_counter() - start
    print("Time elapsed (s)", stop)


if __name__ == "__main__":
    main()
