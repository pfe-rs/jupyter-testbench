import numpy as np
import testbench

def meanPower(x: np.array) -> float:
    y = np.mean(np.square(x))
    return y

def test_meanPower(bench: 'Testbench'):
    f1_vals = np.array([1, 2, -3, 4, -5, 6, 7])
    f2_vals = np.array([4, 6, 2, 8, 9])
    f3_vals = np.array([0.5, 4, -1.2, 3.0])
    bench.assert_eq(bench.function(f1_vals), meanPower(f1_vals))
    bench.assert_eq(bench.function(f2_vals), meanPower(f2_vals))
    bench.assert_eq(bench.function(f3_vals), meanPower(f3_vals))
