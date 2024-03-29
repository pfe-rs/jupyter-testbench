import typing
import inspect
import requests
import json
import os

from .tests import *


class Testbench:

    config: typing.Optional[dict] = None
    author_name: typing.Optional[str] = None

    def __init__(self, func: typing.Callable):

        Testbench.load_config()

        if Testbench.author_name is None:
            print('⛔ Nije postavljeno ime autora!')
            return

        self.function: typing.Optional[typing.Callable] = func
        self.score: typing.Optional[int] = None
        self.passed: int
        self.failed: int

        if self.__run_test():
            self.__show_score()
            self.__publish_score()
        else:
            print('⛔ Funkcija \'%s\' ne može da se testira! Proverite da li se dobro zove.' %
                  self.function.__name__)

    def __run_test(self) -> bool:
        if self.function is None:
            return False

        self.passed = 0
        self.failed = 0
        test_name: str = 'test_%s' % self.function.__name__

        if test_name in globals():
            globals()[test_name](self)
            self.score = int(self.passed / (self.passed + self.failed) * 100)
            return True
        else:
            self.score = None
            return False

    def __show_score(self):
        if self.score is not None and self.function is not None:
            if self.score == 100:
                print('✅ Funkcija \'%s\' uspešno prolazi sve testove.' %
                      self.function.__name__)
            else:
                print('⚠️ Funkcija \'%s\' uspešno prolazi %i%% testova.' %
                      (self.function.__name__, self.score))

    def __publish_score(self):
        data: dict = {
            'author': self.author_name,
            'score': self.score,
            'code': inspect.getsource(self.function)
        }

        if Testbench.config is not None and self.function is not None and not Testbench.config['offline']:
            try:
                requests.post(
                    '{}/submit/tests/{}'.format(Testbench.config['server'], self.function.__name__), data=json.dumps(data))
            except requests.exceptions.RequestException:
                print('⚠️ Greška pri kontaktiranju servera za praćenje napretka.')

    def assert_expr(self, expr: bool):
        if expr:
            self.passed += 1
        else:
            self.failed += 1

    def assert_eq(self, value, truth):
        if value == truth:
            self.passed += 1
        else:
            self.failed += 1

    def assert_range(self, value: typing.Union[int, float], 
                            truth: typing.Union[int, float], 
                            error: typing.Union[int, float]):
        if value <= truth + error and value >= truth - error:
            self.passed += 1
        else:
            self.failed += 1

    @staticmethod
    def author(name: str):

        if os.getenv('JUPYTERHUB_USER') is not None:
            print('⚠️ Ime autora nije moguće promeniti!')
        else:
            Testbench.author_name = name
            Testbench.load_config()
            Testbench.__publish_author()

    @staticmethod
    def __publish_author():

        data: dict = {
            'author': Testbench.author_name
        }

        if Testbench.config is not None and not Testbench.config['offline']:
            try:
                requests.post(
                    '{}/submit/authors'.format(Testbench.config['server']), data=json.dumps(data))
            except requests.exceptions.RequestException:
                print('⚠️ Greška pri kontaktiranju servera za praćenje napretka.')

    @staticmethod
    def load_config():
        if Testbench.config is None:
            if os.path.isfile('/etc/testbench.json'):
                with open('/etc/testbench.json', 'r') as f:
                    Testbench.config = json.load(f)
            else:
                # Default configuration
                Testbench.config = {
                    'server': 'http://127.0.0.1:8089',
                    'offline': False
                }

        if Testbench.author_name is None and os.getenv('JUPYTERHUB_USER') is not None:
            Testbench.author_name = os.getenv('JUPYTERHUB_USER')
            Testbench.__publish_author()


Testbench.load_config()
