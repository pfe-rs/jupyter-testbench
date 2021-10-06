def test_is_even(bench: 'Testbench'):

    bench.assert_eq(bench.function(0), True)
    bench.assert_eq(bench.function(1), False)
    bench.assert_eq(bench.function(2), True)
    bench.assert_eq(bench.function(3), False)
    bench.assert_eq(bench.function(2468), True)
    bench.assert_eq(bench.function(12345), False)
