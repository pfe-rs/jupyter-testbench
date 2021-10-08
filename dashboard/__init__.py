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

    authors: list[str] = []

    def __init__(self):
        self.board: dict[str, dict[str, (int, str, int)]] = {}
        for t in self.__get_test_names():
            self.board[t] = {}

    def __get_test_names(self) -> list[str]:
        import testbench
        return list(map(lambda t: t.removeprefix('test_'), filter(lambda fn: fn.startswith('test_'), dir(testbench))))

    def list_tests(self) -> list[str]:

        return list(self.board.keys())

    def list_authors(self) -> list[str]:

        Scoreboard.authors.sort()
        return Scoreboard.authors

    def list_submissions(self, test: str) -> list[(str, int, str)]:

        if not test in self.board.keys():
            return []

        submissions = []
        for author in self.board[test]:
            submissions.append(
                (author, *self.board[test][author])
            )

        submissions.sort(
            key=lambda s: s[1] if s[1] is not None else -1, reverse=True)

        return submissions

    def insert_submission(self, test: str, data: dict) -> bool:

        if not test in self.board.keys():
            # Add unknown tests
            self.board[test] = {}

        if 'author' in data.keys() and 'score' in data.keys() and 'code' in data.keys():
            attempts: int = 1
            if data['author'] in self.board[test]:
                attempts = self.board[test][data['author']][2] + 1
            else:
                Scoreboard.authors.append(data['author'])
                self.add_known_authors([data['author']])

            self.board[test][data['author']] = (
                data['score'], data['code'], attempts)
            return True

        return False

    def insert_author(self, data: dict) -> bool:

        if not 'author' in data.keys():
            return False

        author = data['author']

        if author in Scoreboard.authors:
            return False

        Scoreboard.authors.append(author)

        self.add_known_authors([author])

        return True

    def add_known_authors(self, authors: list[str], test=None):

        if test is None:
            for test in self.board:
                for author in authors:
                    if author not in self.board[test].keys():
                        self.board[test][author] = (None, '', 0)

        else:
            for author in authors:
                if author not in self.board[test].keys():
                    self.board[test][author] = (None, '', 0)

    def reset_test(self, test: str):

        if test in self.__get_test_names():
            self.board[test] = {}
            self.add_known_authors(self.authors, test)
        else:
            self.board.pop(test)

    def reset_all_tests(self):

        self.__init__()
        self.add_known_authors(Scoreboard.authors)

    def reset_all_authors(self):

        for test in self.board:
            for author in Scoreboard.authors:
                if author in self.board[test].keys():
                    if self.board[test][author][0] == None:
                        self.board[test].pop(author)

        Scoreboard.authors = []


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


@ app.route("/authors", methods=['GET'])
def authors_all():
    if request.method == 'GET':
        return render_template("authors.html", authors=board.list_authors())
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


@ app.route("/submit/authors", methods=['POST'])
def submit_authors():
    if request.method == 'POST':
        if board.insert_author(json.loads(request.data)):
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


@ app.route("/reset/authors", methods=['POST'])
def reset_authors_all():
    if request.method == 'POST':
        board.reset_all_authors()
        return redirect('/authors', 302)


if __name__ == '__main__':

    load_config()
    app.run(host=config['host'], port=config['port'], debug=config['debug'])
