# hello.py

from flask import Flask, request, url_for, redirect, abort

app = Flask(__name__)

statistic_data = {}

# -------------------------------------------------------


def load_user(uid):
    try:
        uid = int(uid)
        if uid == 1:
            return "Maomao"
        elif uid == 2:
            return "Alicia"
    except BaseException:
        return

# -------------------------------------------------------


@app.route('/')
def index():
    '''Get request information'''

    # Get headers
    user_agent = request.headers.get('User-Agent')
    # Get arguments
    user_name = request.args.get('name')

    return '<p>Your browser is {}</p><p>Your name is {}</p>'.format(user_agent, user_name)


@app.route("/users")
def get_users():
    users = ["Maomao", "Alicia"]
    resp = ["<p>{}</p>".format(user) for user in users]
    resp = "\n".join(resp)

    return resp


# Dynamic route
@app.route("/user/<name>")
def get_user_name(name):
    return "<h1>Hello, {}!</h1>".format(name)


# Dynamic route
@app.route("/user/<int:uid>")
def get_user_id(uid):
    if isinstance(uid, int):
        return "<h1>Your ID: {}</h1>".format(uid)
    return "<h1>ID should be int</h1>"


# Dynamic route
@app.route("/user/<path:path>")
def get_user_path(path):
    return "<h1>Path: {}</h1>".format(path)


@app.route("/check_user/<uid>")
def check_user(uid):
    user = load_user(uid)

    if not user:
        '''
        Return specific HTTP status code
            - client error: 4xx
            - server error: 5xx
        '''
        abort(400) 
    else:
        return "<h1>Hello, {}!</h1>".format(user)


@app.route('/redirect')
def redirect_google():
    # return '<h1>Redirect</h1>', 302, {'Location': 'http://www.google.com'}
    return redirect("http://www.google.com")


@app.route('/has_cookie')
def has_cookie():
    data = '<h1>This document carries a cookie!</h1>', 200, {'Set-Cookie': 'answer=45'}

    # Set cookie: method 1
    # headers = {}
    # headers['Set-Cookie'] = 'answer=45'
    # return Response(data, headers=headers)

    # Set cookie : method 2 - from response object
    res = app.make_response(data)
    res.set_cookie('answer', '1234', expires=1516717980)
    return res


@app.before_request
def count():
    '''Request hooks.
    
    - `before_first_request`: Register a function to run before the first request is handled.
    - `before_request`: Register a function to run before each request.
    - `after_request`: Register a function to run after each request, if no unhandled exceptions occurred.
    - `teardown_request`: Register a function to run after each request, even if unhandled exceptions occurred.
    '''

    if request.path in [url_for('buy_food'), url_for('buy_drink')]:
        item = request.path.rsplit('/', 1)[-1]
        statistic_data[item] = statistic_data.setdefault(item, 0) + 1


@app.route('/statistic')
def get_statistic():
    return 'statistic_data: {}'.format(statistic_data)


@app.route('/buy/food')
def buy_food():
    return '<p>Here is your food.</p>'


@app.route('/buy/drink')
def buy_drink():
    return '<p>Here is your drink.</p>'


@app.route("/error")
def error():
    raise RuntimeError


if __name__ == '__main__':
    app.run(threaded=True, debug=True, port=5000)
