#!/usr/bin/env python

from flask import Flask, request, render_template, redirect, url_for, Response
import json
import pickle
import typing
import os
import pkgutil
import sys
from datetime import datetime
sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))


def load_config() -> typing.Optional[dict]:
    if os.path.isfile('/etc/dashboard.json'):
        with open('/etc/dashboard.json', 'r') as f:
            return json.load(f)
    else:
        # Default configuration
        return {
            'host': '127.0.0.1',
            'port': 8089,
            'debug': True
        }


def load_users() -> dict[str, str]:
    users: list[dict[str, str]] = []
    if os.path.isfile('/etc/users.json'):
        with open('/etc/users.json', 'r') as f:
            users = json.load(f)
    ret: dict[str, str] = {}
    for user in users:
        ret[user['username']] = user['name']
    return ret


class Scoreboard:

    authors: list[str] = []

    def __init__(self):
        # test -> author -> (score, code, attempts)
        self.board: dict[str, dict[str,
                                   typing.Tuple[typing.Optional[int], str, int]]] = {}
        for t in self.__get_test_names():
            self.board[t] = {}
        user_list: list[str] = list(users.values())
        self.add_known_authors(user_list)
        Scoreboard.authors = user_list

    def __get_test_names(self) -> list[str]:
        module_path: str = os.path.dirname(
            pkgutil.get_loader('testbench').get_filename())
        tests_path = os.path.join(module_path, 'tests')
        return sorted([test[:-3] for test in os.listdir(tests_path) if test.endswith('.py') and test != '__init__.py'])

    def list_tests(self) -> list[str]:

        return list(self.board.keys())

    def list_authors(self) -> list[str]:

        Scoreboard.authors.sort()
        return Scoreboard.authors

    def list_submissions(self, test: str) -> list[typing.Tuple[str, int, str]]:

        if not test in self.board:
            return []

        submissions = []
        for author in self.board[test]:
            submissions.append(
                (author, *self.board[test][author])
            )

        submissions.sort(
            key=lambda s: s[1] if s[1] is not None else -1, reverse=True)

        return submissions

    def list_author_submissions(self, author: str) -> list[typing.Tuple[str, typing.Optional[int], str, int]]:
        return [(test, *self.board[test][author]) for test in sorted(list(self.board.keys()))]

    def get_author_name_override(self, author: str) -> str:
        if author in users:
            return users[author]
        return author

    def insert_submission(self, test: str, data: dict) -> bool:

        if not test in self.board.keys():
            # Add unknown test
            self.board[test] = {}
            self.add_known_authors(Scoreboard.authors, test=test)

        if 'author' in data and 'score' in data and 'code' in data:
            attempts: int = 1

            author: str = self.get_author_name_override(data['author'])

            if author in self.board[test]:
                attempts = self.board[test][author][2] + 1

            if author not in Scoreboard.authors:
                Scoreboard.authors.append(author)
                self.add_known_authors([author])

            self.board[test][author] = (
                data['score'], data['code'], attempts)

            return True

        return False

    def insert_author(self, data: dict) -> bool:

        if not 'author' in data.keys():
            return False

        author = self.get_author_name_override(data['author'])

        if author in Scoreboard.authors:
            return False

        if author not in Scoreboard.authors:
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
                if author in self.board[test]:
                    if self.board[test][author][0] == None:
                        self.board[test].pop(author)

        Scoreboard.authors = []

    def reset_author(self, author):

        for test in self.board:
            if author in self.board[test]:
                self.board[test].pop(author)

        Scoreboard.authors.remove(author)


app = Flask(__name__)
users: dict[str, str] = load_users()
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


@ app.route("/authors/<string:author>", methods=['GET'])
def author_specified(author):
    if request.method == 'GET':
        return render_template("author.html", author=author, submissions=board.list_author_submissions(author))
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


@ app.route("/reset/tests", methods=['GET'])
def reset_tests_all():
    if request.method == 'GET':
        board.reset_all_tests()
        return redirect(url_for('tests_all'), 302)
    return 'Err'


@ app.route("/reset/tests/<string:test>", methods=['GET'])
def reset_tests_specified(test):
    if request.method == 'GET':
        board.reset_test(test)
        return redirect(url_for('tests_specified', test=test), 302)
    return 'Err'


@ app.route("/reset/authors", methods=['GET'])
def reset_authors_all():
    if request.method == 'GET':
        board.reset_all_authors()
        board.reset_all_tests()
        return redirect(url_for('authors_all'), 302)
    return 'Err'


@ app.route("/reset/authors/<string:author>", methods=['GET'])
def reset_authors_specified(author):
    if request.method == 'GET':
        board.reset_author(author)
        return redirect(url_for('authors_all'), 302)
    return 'Err'


@ app.route("/export", methods=['GET'])
def export_scoreboard():
    if request.method == 'GET':
        r = Response(
            json.dumps({
                'authors': Scoreboard.authors,
                'scoreboard': board.board
            }),
            mimetype='application/json',
        )
        t = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        r.headers[
            'Content-Disposition'] = f'attachment; filename="testbench_dashboard_{t}"'
        return r
    else:
        return 'Err'


@ app.route("/import", methods=['GET', 'POST'])
def import_scoreboard():
    if request.method == 'GET':
        return render_template("import.html")
    elif request.method == 'POST':
        keep = 'keepExisting' in request.form
        upload = request.files['scoreboardFile']
        obj = json.loads(upload.stream.read())
        if keep:
            Scoreboard.authors = list(set(
                Scoreboard.authors + obj['authors']
            ))
            for test_name in obj['scoreboard']:
                if test_name in board.board:
                    board.board[test_name] |= obj['scoreboard'][test_name]
                else:
                    board.board[test_name] = obj['scoreboard'][test_name]
        else:
            Scoreboard.authors = obj['authors']
            board.board = obj['scoreboard']
        return redirect(url_for('root'), 302)
    else:
        return 'Err'


if __name__ == '__main__':
    config: typing.Optional[dict] = load_config()
    if config is not None:
        app.run(host=config['host'], port=config['port'],
                debug=config['debug'])
