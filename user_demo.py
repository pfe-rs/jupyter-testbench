#!/usr/bin/env python

import numpy as np
from testbench import Testbench

Testbench.author('Petar Petrović')


def heart_beats(data: np.array) -> int:
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


def zbirTriSinusoide(f1: float, f2: float, f3: float, A1: float, A2: float, A3: float) -> np.array:
    t = np.linspace(0, 3, 3 * 10000)
    x1 = A1 * np.sin(f1 * 2 * np.pi * t)
    x2 = A2 * np.sin(f2 * 2 * np.pi * t)
    x3 = A3 * np.sin(f3 * 2 * np.pi * t)
    return x1 + x2 + x3

if __name__ == '__main__':
    Testbench(heart_beats)
    Testbench(zbirTriSinusoide)