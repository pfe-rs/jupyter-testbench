#!/usr/bin/env python

from flask import Flask, request, render_template
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
        self.board: dict[str, dict[str, (int, str)]] = {}
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
            self.board[test][data['author']] = (data['score'], data['code'])
            return True

        return False


app = Flask(__name__)
board = Scoreboard()


@ app.route("/", methods=['GET'])
def root():
    return render_template("root.html")


@ app.route("/tests", methods=['GET'])
def tests_all():
    if request.method == 'GET':
        return render_template("tests.html", tests=board.list_tests())


@ app.route("/tests/<string:test>", methods=['GET', 'POST'])
def tests_specified(test):
    if request.method == 'GET':
        return render_template("test.html", test=test, submissions=board.list_submissions(test))
    elif request.method == 'POST':
        if board.insert_submission(test, json.loads(request.data)):
            return 'Ok'
        else:
            return 'Err'


if __name__ == '__main__':

    load_config()
    app.run(host=config['host'], port=config['port'], debug=config['debug'])
