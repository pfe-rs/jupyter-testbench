import numpy as np
import testbench

def squarePower(x: np.array) -> np.array:
    return x**2


def test_squarePower(bench: 'Testbench'):
    #TREBA DA SE IMPLEMENTIRAJU PRAVI PRIMERI
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    f1_vals = [0.5, 1, 4]
    f2_vals = [2, 0.8, 1]
    f3_vals = [3, 4, 5]
    A1_vals = [3, 2, 0.7]
    A2_vals = [1, 2, 4]
    A3_vals = [1, 5, 10]
    bench.assert_expr(np.array_equal(bench.function(1,1,1,1,1,1), squarePower(1,1,1,1,1,1)))