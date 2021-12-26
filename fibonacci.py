#!/usr/bin/env python3

"""
The original fibonacci function calculates the same f(n) many times. A first gain in performance would be to store previously calculated numbers in memory, 
in order to access those instead of calculating again. Then the fibonacci recursive function could be left as is and it would work much faster, but would soon 
run into a problem with recursion depth with bigger numbers (e.g. n=100000). In order to fix the latter, I iterate from 0 to n calculating and storing the fibonacci number,
this way the maximum recursion depth is kept at a maximum of 1.
"""

import time

fibos = {
    0: 0,
    1: 1
}
    
def calculate_fibonacci(n, depth=0):
    global fibos

    if (n < 0):
        raise NotImplementedError("Only positive numbers allowed")
    if (n < 2):
        return n, depth

    if n in fibos:
        return fibos[n], depth

    calculated = calculate_fibonacci(n-1, depth=depth+1)[0] + calculate_fibonacci(n-2, depth=depth+1)[0]
    fibos[n] = calculated

    return calculated, depth
  
def optimized_fibonacci(n):
    global fibos

    # Iterate up to n, checking if n exists in our global dictionary storage, if the fibonacci for that number is not stored, then calculate it
    for i in range(n):
        if (i not in fibos):
            fibos[i], _ = calculate_fibonacci(i)

    r,_ = calculate_fibonacci(n)

    return r   


def last_8(some_int):
    """Return the last 8 digits of an int

    :param int some_int: the number
    :rtype: int
    """

    return int(str(some_int)[-8:])


class SummableSequence(object):
    def __init__(self, *initial):
        raise NotImplementedError()

    def __call__(self, i):
        raise NotImplementedError()


if __name__ == "__main__":

    t0 = time.perf_counter()        
    print("f(100000)[-8:]", last_8(optimized_fibonacci(100000)))
    t1 = time.perf_counter()  - t0
    print("Time elapsed (s)",t1)

    #new_seq = SummableSequence(5, 7, 11)
    #print("new_seq(100000)[-8:]:", last_8(new_seq(100000)))
