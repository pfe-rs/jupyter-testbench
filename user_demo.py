#!/usr/bin/env python

import cv2
import numpy as np
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


def binarization(image: np.ndarray) -> np.ndarray:
    threshold = 128 # 127 for 33% correctness, 129 for 66% correctness
    image_grayscale: np.ndarray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, image_threshold = cv2.threshold(image_grayscale, threshold, 255, cv2.THRESH_BINARY)
    return image_threshold


if __name__ == '__main__':
    Testbench(fibonacci)
    Testbench(factorial)
    Testbench(is_even)
    Testbench(binarization)
