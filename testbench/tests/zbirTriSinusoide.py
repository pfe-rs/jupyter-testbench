import numpy as np
import testbench

def zbirTriSinusoide(f1: float, f2: float, f3: float, A1: float, A2: float, A3: float) -> np.array:
    t = np.linspace(0, 3, 3 * 10000)
    x1 = A1 * np.sin(f1 * 2 * np.pi * t)
    x2 = A2 * np.sin(f2 * 2 * np.pi * t)
    x3 = A3 * np.sin(f3 * 2 * np.pi * t)
    return x1 + x2 + x3


def test_zbirTriSinusoide(bench: 'Testbench'):
    f1_vals = [0.5, 1, 4]
    f2_vals = [2, 0.8, 1]
    f3_vals = [3, 4, 5]
    A1_vals = [3, 2, 0.7]
    A2_vals = [1, 2, 4]
    A3_vals = [1, 5, 10]
    for f1, f2,  f3, A1, A2, A3 in zip(f1_vals, f2_vals, f3_vals, A1_vals, A2_vals, A3_vals):
        bench.assert_expr(np.array_equal(bench.function(f1,f2,f3,A1,A2,A3), zbirTriSinusoide(f1,f2,f3,A1,A2,A3)))
    