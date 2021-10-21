import numpy as np
import testbench

def signalFormation(f1: float, f2: float, f3: float, A1: float, A2: float, A3: float) -> np.array:
    t = np.linspace(0, 3, 3 * 10000)
    x1 = A1 * np.sin(f1 * 2 * np.pi * t)
    x2 = A2 * np.sin(f2 * 2 * np.pi * t)
    x3 = A3 * np.sin(f3 * 2 * np.pi * t)
    return x1 + x2 + x3


def test_signalFormation(bench: 'Testbench'):
    f1 = [0.5, 1, 4]
    f2 = [2, 0.8, 1]
    f3 = [3, 4, 5]
    A1 = [3, 2, 0.7]
    A2 = [1, 2, 4]
    A3 = [1, 5, 10]

    for params in zip(f1, f2, f3, A1, A2, A3):
        bench.assert_expr(np.array_equal(bench.function(*params), signalFormation(*params)))
    