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


if __name__ == '__main__':
    Testbench(fibonacci)
