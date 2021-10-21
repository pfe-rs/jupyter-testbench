import numpy as np
from scipy.io import wavfile

def shiftSignal(x, K):
    N = len(x)
    y = np.zeros(N)
    if K < 0:
        y[:N + K] = x[-K:N]
    else:
        y[K:N] = x[:N-K]
    return y

def cutShiftSignal(x: np.array, K: float, S: float) -> np.array:
    y = x[S:]
    y1 = shiftSignal(y, K)
    return y1


def test_cutShiftSignal(bench: 'Testbench'):
    fs, x = wavfile.read('datasets/guitar_sound/skala.wav')
    bench.assert_expr(np.array_equal(bench.function(x, 1, 1), cutShiftSignal(x, 1, 1)))
  