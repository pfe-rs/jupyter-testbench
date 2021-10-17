def heart_beats(bench: 'Testbench'):
    bench.assert_eq(bench.function('testbench.tests.datasets.heart.ECG.dat'), 24)

