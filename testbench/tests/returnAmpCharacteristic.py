import numpy as np
from scipy.fft import fft

def returnAmpCharacteristic(x: np.array) -> np.array:
    amp_spectrum = np.abs(fft(x))
    return amp_spectrum


def test_returnAmpCharacteristic(bench: 'Testbench'):
    x1 = np.zeros(10)
    x2 = np.sin(np.linspace(0, 5, 50))
    
    bench.assert_expr(np.array_equal(bench.function(x1), returnAmpCharacteristic(x1)))
    bench.assert_expr(np.array_equal(bench.function(x2), returnAmpCharacteristic(x2)))