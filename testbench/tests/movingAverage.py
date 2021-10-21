import numpy as np

def movingAverage(x: np.array, w: int) -> np.array:
    smoothed = np.zeros(len(x) - w + 1)
    # ovde je potrebno implementirati zadatu funkciju
    for i in range(len(x) - w + 1):
        smoothed[i] = np.mean(x[i:i+w])
    return smoothed


def test_movingAverage(bench: 'Testbench'):
    t = np.linspace(0, 100, 1000)
    x1 = 10 * np.sin(15 * 2 * np.pi * t) + 3 * np.sin(4 * 2 * np.pi * t)
    x2 = 4 * np.cos(5 * 2 * np.pi * t) + 7 * np.sin(5 * 2 * np.pi * t)

    bench.assert_expr(np.array_equal(bench.function(x1, 2), movingAverage(x1, 2)))
    bench.assert_expr(np.array_equal(bench.function(x2, 100), movingAverage(x2, 100)))