# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring


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
    optimized_calculate_seq,
    optimized_fibonacci,
)
from pyramid import print_pyramid
import fibonacci
import pyramid


try:
    # Absent on Windows, trigger AttributeError

    signal.alarm  # pylint: disable=pointless-statement

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
            with timeout(message=f"Timeout running f({n})"):
                self.assertEqual(expected, optimized_fibonacci(n))

    def test_optimized_calculate_seq_asserts(self):
        with self.assertRaises(AssertionError):
            _ = [
                # i, n must be 0 or more
                optimized_calculate_seq(-1, [1, 2, 4]),
                optimized_calculate_seq(3, [1, 2, 4], n=-1),
                # n must be equal or smaller than len(initial)
                optimized_calculate_seq(3, [1, 2, 4], n=5),
            ]

    def test_optimized_calculate_seq_none_n(self):
        self.assertEqual(optimized_calculate_seq(3, [1, 2, 4], n=None), 7)

    def test_summable(self):
        ss = SummableSequence(0, 1)
        for n in range(0, 50, 5):
            with timeout(message=f"Timeout running f({n})"):
                self.assertEqual(ss(n), optimized_fibonacci(n))

    def test_summable_n(self):
        # Checks that the n rule (where the i-th number is the
        # sum of the previous n numbers in the sequence) is
        # working propery. We can do this predictably with an array of ones
        for n in range(1, 50, 5):
            ones = [1 for _ in range(n)]
            ss = SummableSequence(*ones)
            with timeout(message=f"Timeout running f({n})"):
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
            with timeout(message=f"Timeout running f({n})"):
                self.assertEqual(expected, ss(n))

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
