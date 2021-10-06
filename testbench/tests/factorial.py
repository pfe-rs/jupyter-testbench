def test_factorial(bench: 'Testbench'):

    bench.assert_eq(bench.function(0), 1)
    bench.assert_eq(bench.function(1), 1)
    bench.assert_eq(bench.function(2), 2)
    bench.assert_eq(bench.function(3), 6)
    bench.assert_eq(bench.function(5), 120)
