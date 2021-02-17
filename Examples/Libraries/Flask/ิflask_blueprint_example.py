# # #--------exmaple1
# #Register a blueprint multiple times on an application with differne URL.
# from flask import Flask
# from flask import Blueprint, render_template, abort
# from jinja2 import TemplateNotFound

# app = Flask(__name__)

# simple_page = Blueprint('simple_page', __name__,
#                         template_folder='templates')

# @simple_page.route('/', defaults={'page': 'index'}) # what is default for?
# @simple_page.route('/<page>')
# def show(page):
#     try:
#         return render_template('pages/%s.html' % page)
#     except TemplateNotFound:
#         abort(404)

# --------exmaple2

from flask import Flask
from flask import Blueprint, render_template, abort

simple_page = Blueprint("simple_page", __name__, template_folder="templates")


@simple_page.route("/", defaults={"page": "index"})  # what is default for?
@simple_page.route("/anak/<page>")
def show(page):
    return page
    # print('pages/%s.html' % page)
    #     return render_template('pages/%s.html' % page)
    # except TemplateNotFound:
    #     abort(404)


app = Flask(__name__)
app.register_blueprint(simple_page)  # what does ti do?

# print(app.url_map)
# print(simple_page.root_path)

# -- example 3
# quickly open this foldre
# with simple_page.open_resource('static/style.css') as f:
#     code = f.read()


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)
    # app.run(host='127.0.01', port=5000, debug=True)
