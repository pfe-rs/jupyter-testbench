#!/usr/bin/env python

import numpy as np
from testbench import Testbench

Testbench.author('Petar Petrović')


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    root = int(np.sqrt(n))
    for i in range(2, root + 1):
        if n % i == 0:
            return False
    return True


def heart_beats(name: str) -> int:
    data = np.fromfile(name, dtype=int)
    signal = np.diff(data)
    br = 0
    i = 0
    while i < np.size(signal)-1:
        if signal[i] > 500000:
            br = br+1
            i = i + 100
        else:
            i = i + 1
    return br


if __name__ == '__main__':
    Testbench(is_prime)
    Testbench(heart_beats)
