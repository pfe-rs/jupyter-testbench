import typing


class Testbench:

    def __init__(self, func: typing.Callable):
        self.function: str = func
        self.passed: int = 0
        self.failed: int = 0

        test_name: str = 'test_%s' % self.function.__name__
        if test_name in globals():
            globals()[test_name](self)
            test_score: int = self.passed / (self.passed + self.failed) * 100

            print('%s Funkcija \'%s\' uspešno prolazi %i%% testova.' %
                  ('✅' if test_score == 100 else '⚠️', self.function.__name__, test_score))
        else:
            print('⛔ Funkcija \'%s\' ne može da se testira!' %
                  self.function.__name__)

    def assert_eq(self, value, truth):
        if value == truth:
            self.passed += 1
        else:
            self.failed += 1


def test_fibonacci(bench: Testbench):

    bench.assert_eq(bench.function(0), 0)
    bench.assert_eq(bench.function(1), 1)
    bench.assert_eq(bench.function(2), 1)
    bench.assert_eq(bench.function(3), 2)
    bench.assert_eq(bench.function(5), 5)
    bench.assert_eq(bench.function(20), 6765)
