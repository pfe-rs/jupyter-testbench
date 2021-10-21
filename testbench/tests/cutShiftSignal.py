import numpy as np
import testbench

def cutShiftSignal(x: np.array, K: float, S: float) -> np.array:
    y = x[S:]
    y1 = shiftSignal(y, K)
    return y1


def test_cutShiftSignal(bench: 'Testbench'):
    #TREBA DA SE IMPLEMENTIRAJU PRAVI PRIMERI
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    f1_vals = [0.5, 1, 4]
    f2_vals = [2, 0.8, 1]
    f3_vals = [3, 4, 5]
    A1_vals = [3, 2, 0.7]
    A2_vals = [1, 2, 4]
    A3_vals = [1, 5, 10]
    bench.assert_expr(np.array_equal(bench.function(1,1,1,1,1,1), cutShiftSignal(1,1,1,1,1,1)))
    