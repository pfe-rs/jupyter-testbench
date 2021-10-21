import numpy as np
import testbench

def squarePower(x: np.array) -> np.array:
    return x**2


def test_squarePower(bench: 'Testbench'):
    f1_vals = np.array([1, 2, -3, 4, -5, 6, 7])
    f2_vals = np.array([4, 6, 2, 8, 9])
    f3_vals = np.array([0.5, 4, -1.2, 3.0])
    bench.assert_expr(np.array_equal(bench.function(f1_vals), squarePower(f1_vals)))
    bench.assert_expr(np.array_equal(bench.function(f2_vals), squarePower(f2_vals)))
    bench.assert_expr(np.array_equal(bench.function(f3_vals), squarePower(f3_vals)))