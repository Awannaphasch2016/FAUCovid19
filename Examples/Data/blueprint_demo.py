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


if __name__ == "__main__":
    app.run(debug=True)
