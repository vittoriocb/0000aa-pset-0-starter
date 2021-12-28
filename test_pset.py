# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=invalid-name

"""
Test suites for the assignment
"""

import signal
import sys
from contextlib import contextmanager
from io import StringIO
from time import sleep, time
from unittest import TestCase, main

from fibonacci import (
    SummableSequence,
    last_8,
    optimized_fibonacci,
    optimized_calculate_seq,
    sum_sequence,
)
from pyramid import print_pyramid
import fibonacci
import pyramid


try:
    # Absent on Windows, trigger AttributeError
    # pylint: disable=pointless-statement
    signal.alarm

    def _timeout(signum, frame):
        raise TimeoutError()

    signal.signal(signal.SIGALRM, _timeout)

    @contextmanager
    def timeout(seconds=1, message="Timeout!"):
        # NB: doesn't work on windows
        signal.alarm(seconds)
        try:
            yield
        except TimeoutError as timeout_error:
            raise TimeoutError(message) from timeout_error
        finally:
            signal.alarm(0)

except AttributeError:

    @contextmanager
    def timeout(seconds=1, message="Timeout!"):
        t0 = time()
        yield
        if time() - t0 > seconds:
            raise TimeoutError(message)


@contextmanager
def capture_print():
    _stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        yield sys.stdout
    finally:
        sys.stdout = _stdout


class FibTests(TestCase):
    def test_fibonnacci(self):
        for n, expected in [
            # Check progressively more complex values, see if time out
            (0, 0),
            (1, 1),
            (6, 8),
            (10, 55),
            (15, 610),
            (20, 6765),
            (30, 832040),
            (40, 102334155),
            (100, 354224848179261915075),
        ]:
            with timeout(message="Timeout running f({})".format(n)):
                self.assertEqual(expected, optimized_fibonacci(n))

    def test_no_negative(self):
        with self.assertRaises(ValueError):
            optimized_fibonacci(-1)

    def test_check_n(self):
        with self.assertRaises(ValueError):
            optimized_calculate_seq(5, num=5, initial=[0, 1])

    def test_summable(self):
        ss = SummableSequence(0, 1)
        for n in range(0, 50, 5):
            with timeout(message="Timeout running f({})".format(n)):

                self.assertEqual(ss(n), optimized_fibonacci(n))

    def test_summable_n(self):
        # Checks that the n rule (where the i-th number is the
        # sum of the previous n numbers in the sequence) is
        # working propery. We can do this predictably with an array of ones
        for n in range(1, 50, 5):
            ones = [1 for _ in range(n)]
            ss = SummableSequence(*ones)
            with timeout(message="Timeout running f({})".format(n)):
                self.assertEqual(ss(n), n)

    def test_summable_calc(self):
        ss = SummableSequence(5, 7, 11)
        for n, expected in [
            # Check progressively more complex values, see if time out
            (0, 5),
            (1, 7),
            (2, 11),
            (10, 1587),
            (16, 61445),
            (20, 703209),
            (30, 311586659),
        ]:
            with timeout(message="Timeout running f({})".format(n)):
                self.assertEqual(expected, ss(n))

    def test_sum_sequence(self):
        for seq, expected in [
            # Check progressively more complex values, see if time out
            ([1, 2, 3], 6),
            ([5, 5, 5], 15),
            ([9, 5], 14),
            ([2, 10, 8, 20], 40),
        ]:
            self.assertEqual(expected, sum_sequence(len(seq), seq))

    def test_main(self):
        # Just check there is output and no exceptions
        with capture_print() as std:
            fibonacci.main()

        std.seek(0)
        captured = std.read()

        self.assertEqual(len(captured) > 0, True)


class TestTimeout(TestCase):
    def test_timeout(self):
        with self.assertRaises(TimeoutError):
            with timeout():
                sleep(2)


class MiscTests(TestCase):
    def test_8(self):
        self.assertEqual(123, last_8(123))
        self.assertEqual(23456789, last_8(123456789))


class PyramidTests(TestCase):
    def _assert_expected(self, rows, expected):
        with capture_print() as std:
            print_pyramid(rows)

        std.seek(0)
        captured = std.read()

        self.assertEqual(expected, captured)

    def test_pyramid_one(self):
        self._assert_expected(1, "=\n")

    def test_pyramid_two(self):
        self._assert_expected(2, "-=-\n" + "===\n")

    def test_nonint_error(self):
        with self.assertRaises(ValueError):
            print_pyramid("test")

    def test_main(self):
        sys.argv = ["--rows 5"]
        # Just check there is output and no exceptions
        with capture_print() as std:
            pyramid.main()

        std.seek(0)
        captured = std.read()

        self.assertEqual(len(captured) > 0, True)
        sys.argv = []


if __name__ == "__main__":
    main()
