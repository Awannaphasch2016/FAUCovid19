from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)

# 2.create 3 function where keywords will determine which combination of the three will be called.
# 	/keyword
# 	/twitter_cralwer
# 	/end_date


@app.route("/keyword", methods=["GET"])
def get_keyword():
    pass


@app.route("/crawler_type", methods=["GET"])
def get_keyword():
    pass


@app.route("/end_date", methods=["GET"])
def get_keyword():
    pass
