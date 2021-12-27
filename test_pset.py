import signal
import sys
from contextlib import contextmanager
from io import StringIO
from time import sleep, time
from unittest import TestCase, main

from fibonacci import SummableSequence, last_8, optimized_fibonacci, optimized_calculate_seq
from pyramid import print_pyramid

try:
    # Absent on Windows, trigger AttributeError
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
        except TimeoutError:
            raise TimeoutError(message)
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
            optimized_calculate_seq(5, n=5, initial=[0,1])

    def test_summable(self):
        ss = SummableSequence(0, 1)
        for n in range(0, 50, 5):
            with timeout(message="Timeout running f({})".format(n)):

                self.assertEqual(ss(n), optimized_fibonacci(n))
    
    def test_summable_n(self):
        # Checks that the n rule (where the i-th number is the sum of the previous n numbers in the sequence) is working propery. We can do this predictably with an array of ones
        for n in range(1, 50, 5):
            ones = [1 for _ in range(n)]
            ss = SummableSequence(*ones)
            with timeout(message="Timeout running f({})".format(n)):
                self.assertEqual(ss(n), n)

    ## TODO: Implement more SummableSequence tests


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
            print_pyramid('test')


if __name__ == "__main__":
    main()
