def test_is_prime(bench: 'Testbench'):

    bench.assert_eq(bench.function(2), True)
    bench.assert_eq(bench.function(4), False)

