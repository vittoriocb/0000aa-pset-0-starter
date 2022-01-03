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


def optimized_calculate_seq(i, initial, n=None):
    """Calculates a sequence of numbers where the ith number is the sum of the
    previous n numbers in the sequence, with the first n numbers defined
    arbitrarily.

    :param int i: position of number to calculate
    :param int n: amount of previous numbers to sum at ith position
    :param list(int) initial: arbitrary intial sequence of numbers
    :rtype: int
    """
    # I was not sure whether n could be defined arbitrarily or is always len(initial)
    # so I added the optional parameter for more flexibility

    len_initial = len(initial)
    # Default n to len(initial) if None
    n = n or len_initial

    # Single assert, reduces cyclomatic complexity
    assert (
        i >= 0 and 0 <= n <= len_initial
    ), "i, n must be 0 or more, and n must be equal or smaller than len(initial)"

    # If i is in the initial list of numbers then there is no need to calculate it
    if i < len_initial:
        return initial[i]

    last_calc = initial.copy()
    for _ in range(len_initial, i + 1):
        # Sum of the last n numbers of the list
        sum_n = sum(last_calc[n * -1 :])
        last_calc.append(sum_n)
        # Keeps list small by removing first element, which is not needed anymore
        last_calc.pop(0)

    result = last_calc[-1]

    return result


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
