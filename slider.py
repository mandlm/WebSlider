#!/usr/bin/python3

from flask import Flask, render_template, send_from_directory, redirect, url_for
from random import randint
from os import listdir
import random

import config

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("hello.html", num=randint(1, 23))


@app.route("/random_image")
def random_image():
    filename = random.choice(listdir(config.imgdir))
    return redirect(url_for("image", filename=filename))


@app.route("/img/<path:filename>")
def image(filename):
    return send_from_directory(config.imgdir, filename)


if __name__ == "__main__":
    app.run()
