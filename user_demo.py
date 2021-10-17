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


import cv2
import numpy as np
def binarization(image: np.ndarray) -> np.ndarray:
    # 127 for 33% correctness, 129 for 66% correctness
    threshold = 128
    image_grayscale: np.ndarray = cv2.cvtColor(
        image, cv2.COLOR_RGB2GRAY
    )
    _, image_threshold = cv2.threshold(
        image_grayscale, 
        threshold, 255, 
        cv2.THRESH_BINARY
    )
    return image_threshold
    

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    root = int(np.sqrt(n))
    for i in range(2, root + 1):
        if n % i == 0:
            return False
    return True

def heart_beats(data: np.array) -> int:
    signal=np.diff(data)
    br = 0
    i = 0
    while i<np.size(signal)-1:
        if signal[i] > 500000:
            br = br+1
            i = i + 100
        else:
            i = i + 1
    return br


if __name__ == '__main__':
    Testbench(fibonacci)
    Testbench(factorial)
    Testbench(is_even)
    Testbench(binarization)
    Testbench(is_prime)
    Testbench(heart_beats)