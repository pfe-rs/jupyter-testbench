import typing
import inspect
import requests
import json


class Testbench:

    author_name: str = None

    def __init__(self, func: typing.Callable):

        if Testbench.author_name is None:
            print('⛔ Nije postavljeno ime autora!')
            return

        self.function: str = func
        self.score: int = None

        if self.__run_test():
            self.__show_score()
        else:
            print('⛔ Funkcija \'%s\' ne može da se testira! Proverite da li se dobro zove.' %
                  self.function.__name__)

    def __run_test(self) -> bool:

        self.passed: int = 0
        self.failed: int = 0
        test_name: str = 'test_%s' % self.function.__name__

        if test_name in globals():
            globals()[test_name](self)
            self.score = int(self.passed / (self.passed + self.failed) * 100)
            return True
        else:
            self.score = None
            return False

    def __show_score(self):
        if self.score is not None:
            if self.score == 100:
                print('✅ Funkcija \'%s\' uspešno prolazi sve testove.' %
                      self.function.__name__)
            else:
                print('⚠️ Funkcija \'%s\' uspešno prolazi %i%% testova.' %
                      (self.function.__name__, self.score))

    def assert_eq(self, value, truth):
        if value == truth:
            self.passed += 1
        else:
            self.failed += 1

    @staticmethod
    def author(name: str):
        Testbench.author_name = name


def test_fibonacci(bench: Testbench):

    bench.assert_eq(bench.function(0), 0)
    bench.assert_eq(bench.function(1), 1)
    bench.assert_eq(bench.function(2), 1)
    bench.assert_eq(bench.function(3), 2)
    bench.assert_eq(bench.function(5), 5)
    bench.assert_eq(bench.function(20), 6765)
