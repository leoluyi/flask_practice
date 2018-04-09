# hello.py

'''Warning

While the maintainers are willing to merge PR’s, they are not actively 
developing features. As of Flask 0.11, Flask includes a built-in CLI tool, and
that may fit your needs better.

http://flask.pocoo.org/docs/0.12/cli/
'''

from flask import Flask
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)


@app.route("/")
def index():
    return "<h1>Hello Word</h1>"


@manager.command
def hello():
    """Just say hello"""
    print("hello")


if __name__ == "__main__":
    manager.run()
