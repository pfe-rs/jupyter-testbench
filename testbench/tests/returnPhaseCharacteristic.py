import numpy as np
from scipy.fft import fft

def returnPhaseCharacteristic(x: np.array) -> np.array:
    phase_spectrum = np.angle(fft(x))
    return phase_spectrum


def test_returnPhaseCharacteristic(bench: 'Testbench'):
    x1 = np.zeros(10)
    x2 = np.sin(np.linspace(0, 5, 50))
    
    bench.assert_expr(np.array_equal(bench.function(x1), returnPhaseCharacteristic(x1)))
    bench.assert_expr(np.array_equal(bench.function(x2), returnPhaseCharacteristic(x2)))