import random
import requests
from flask import render_template
from werkzeug.utils import redirect

from app import app

CODES = list(requests.status_codes._codes)


@app.route("/")
def index():
    return render_template("index.html", codes=CODES)


@app.route("/<code>")
def specific_code(code):
    url = "https://http.cat/{}.jpg".format(code)
    try:
        idx = CODES.index(int(code))
        prec = idx - 1
        suiv = idx + 1 if idx < len(CODES) - 1 else 0
        return render_template("code.html", url=url, codes=CODES, prec=CODES[prec], suiv=CODES[suiv])
    except ValueError:
        return render_template("unknown.html", codes=CODES, code=code)


@app.route("/random")
def random_code():
    code = random.choices(list(CODES))[0]
    return redirect("/{}".format(code), code=302)
