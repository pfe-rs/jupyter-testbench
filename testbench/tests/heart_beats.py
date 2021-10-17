def test_heart_beats(bench: 'Testbench'):
    bench.assert_eq(bench.function('testbench.tests.datasets.heart_beats.ECG.dat'), 24)

