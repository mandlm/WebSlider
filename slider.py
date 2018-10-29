#!/usr/bin/python3

from flask import Flask, render_template
from random import randint

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("hello.html", num=randint(1, 23))


if __name__ == "__main__":
    app.run()
