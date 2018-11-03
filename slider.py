#!/usr/bin/python3

from flask import Flask, render_template, send_from_directory
from random import randint

import config

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("hello.html", num=randint(1, 23))


@app.route("/img/<path:filename>")
def image(filename):
    return send_from_directory(config.imgdir, filename)


if __name__ == "__main__":
    app.run()
