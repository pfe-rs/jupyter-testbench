def test_fibonacci(bench: 'Testbench'):

    bench.assert_eq(bench.function(0), 0)
    bench.assert_eq(bench.function(1), 1)
    bench.assert_eq(bench.function(2), 1)
    bench.assert_eq(bench.function(3), 2)
    bench.assert_eq(bench.function(5), 5)
    bench.assert_eq(bench.function(20), 6765)
