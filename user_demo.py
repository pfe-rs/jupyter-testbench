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


if __name__ == '__main__':
    Testbench(heart_beats)
