# #--------- example 1
# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'hello, world'


# #--------- example 2 
# from markupsafe import escape

# from flask import Flask

# app = Flask(__name__)

# @app.route('/user/<username>')
# def show_user_profile(username):
#     # show the user profile for that user
#     # return 'hi'
#     return 'User %s' % escape(username)

# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     return 'Post %d' % post_id

# @app.route('/path/<path:subpath>')
# def show_subpath(subpath):
#     # show the subpath after /path/
#     return 'Subpath %s' % escape(subpath)

# -------- exmaple3
from flask import Flask, url_for
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    return 'index'

@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(escape(username))

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe')) # redirect useing builtin-keyword "profile" ->"/user/<username>"
    print(url_for('profile'))


# if __name__ == '__main__':
#     # app.run(host='0.0.0.0', port=5000, debug=True)
#     app.run(debug=True)
