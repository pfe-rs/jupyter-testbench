import numpy as np

def skaliranje_signala(signal: np.array, koef: float) -> np.array:
    y_skalirano = koef*signal

    return y_skalirano

def test_skaliranje_signala(bench: 'Testbench'):
    x1 = np.array([1,4,2])
    x2 = np.array([0,0,0])
    bench.assert_expr(np.array_equal(bench.function(x1, 2), skaliranje_signala(x1, 2)))
    bench.assert_expr(np.array_equal(bench.function(x2, 5), skaliranje_signala(x2, 5)))