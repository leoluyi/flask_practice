# hello.py

from flask import Flask, request, url_for

app = Flask(__name__)

statistic_data = {}


@app.route('/')
def index():
    # Get headers
    user_agent = request.headers.get('User-Agent')
    # Get arguments
    user_name = request.args.get('name')

    return '<p>Your browser is {}</p><p>Your name is {}</p>'.format(user_agent, user_name)


@app.route('/redirect')
def redirect():
    return '<h1>Redirect</h1>', 302, {'Location': 'http://www.google.com'}


@app.route('/has_cookie')
def has_cookie():
    data = '<h1>This document carries a cookie!</h1>'

    # Set cookie: method 1
    # headers = {}
    # headers['Set-Cookie'] = 'answer=45'

    # Set cookie: method 2
    res = app.make_response(data)
    res.set_cookie('answer', '1234', expires=1516717980)
    return res


@app.before_request
def statistic():
    if request.path in [url_for('buy_food'), url_for('buy_drink')]:
        statistic_data[request.path] = statistic_data.setdefault(request.path, 0) + 1


@app.route('/statistic') 
def get_statistic():
    return 'statistic_data: {}'.format(statistic_data)


@app.route('/buy/food')
def buy_food():
    return '<p>Here is your food.</p>'


@app.route('/buy/drink')
def buy_drink():
    return '<p>Here is your drink.</p>'


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
