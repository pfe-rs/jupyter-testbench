#!/usr/bin/env python
from testbench import Testbench

Testbench.author('Petar Petrović')


def fibonacci(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def factorial(n: int) -> int:
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)


def is_even(n: int) -> bool:
    return n & 1 == 0


if __name__ == '__main__':
    Testbench(fibonacci)
    Testbench(factorial)
    Testbench(is_even)
