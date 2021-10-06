#!/usr/bin/env python

from flask import Flask, request, render_template, redirect
import json
import typing
from dataclasses import dataclass
import os
import sys
from pprint import pprint
sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))


config: dict = None


def load_config():
    global config
    if os.path.isfile('/etc/dashboard.json'):
        with open('/etc/dashboard.json', 'r') as f:
            config = json.load(f)
    else:
        # Default configuration
        config = {
            'host': '127.0.0.1',
            'port': 8089,
            'debug': True
        }


class Scoreboard:

    def __init__(self):
        self.board: dict[str, dict[str, (int, str, int)]] = {}
        for t in self.__get_test_names():
            self.board[t] = {}

    def __get_test_names(self) -> list[str]:
        import testbench
        return list(map(lambda t: t.removeprefix('test_'), filter(lambda fn: fn.startswith('test_'), dir(testbench))))

    def list_tests(self) -> list[str]:

        return list(self.board.keys())

    def list_submissions(self, test: str) -> list[(str, int, str)]:

        if not test in self.board.keys():
            return []

        submissions = []
        for author in self.board[test]:
            submissions.append(
                (author, *self.board[test][author])
            )

        submissions.sort(key=lambda s: s[1], reverse=True)

        return submissions

    def insert_submission(self, test: str, data: dict) -> bool:

        if not test in self.board.keys():
            # Add unknown tests
            self.board[test] = {}

        if 'author' in data.keys() and 'score' in data.keys() and 'code' in data.keys():
            attempts: int = 1
            if data['author'] in self.board[test]:
                attempts = self.board[test][data['author']][2] + 1

            self.board[test][data['author']] = (
                data['score'], data['code'], attempts)
            return True

        return False

    def reset_test(self, test: str):

        if test in self.__get_test_names():
            self.board[test] = {}
        else:
            self.board.pop(test)

    def reset_all_tests(self):

        self.__init__()


app = Flask(__name__)
board = Scoreboard()


@ app.route("/", methods=['GET'])
def root():
    return render_template("root.html")


@ app.route("/tests", methods=['GET'])
def tests_all():
    if request.method == 'GET':
        return render_template("tests.html", tests=board.list_tests())
    else:
        return 'Err'


@ app.route("/tests/<string:test>", methods=['GET'])
def tests_specified(test):
    if request.method == 'GET':
        return render_template("test.html", test=test, submissions=board.list_submissions(test))
    else:
        return 'Err'


@ app.route("/submit/tests/<string:test>", methods=['POST'])
def submit_tests_specified(test):
    if request.method == 'POST':
        if board.insert_submission(test, json.loads(request.data)):
            return 'Ok'
        else:
            return 'Err'
    else:
        return 'Err'


@ app.route("/reset/tests", methods=['POST'])
def reset_tests_all():
    if request.method == 'POST':
        board.reset_all_tests()
        return redirect('/tests', 302)


@ app.route("/reset/tests/<string:test>", methods=['POST'])
def reset_tests_specified(test):
    if request.method == 'POST':
        board.reset_test(test)
        return redirect('/tests/{}'.format(test), 302)


if __name__ == '__main__':

    load_config()
    app.run(host=config['host'], port=config['port'], debug=config['debug'])
