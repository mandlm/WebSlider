#!/usr/bin/python3

from flask import Flask, render_template, send_from_directory, redirect, url_for
from os import listdir, makedirs
from random import choice
from pathlib import Path
from PIL import Image

import config

app = Flask(__name__)


@app.route("/")
def random():
    return render_template("random.html", refresh=config.refresh)


@app.route("/random_image/")
def random_image():
    filename = choice(listdir(config.imgdir))
    return redirect(url_for("image", filename=filename))


@app.route("/img/<path:filename>")
def image(filename):
    scaled_img_dir = Path(config.imgdir) / ".slider" / "fhd"
    if not scaled_img_dir.exists():
        makedirs(scaled_img_dir)
    if not (scaled_img_dir / filename).exists():
        img = Image.open(Path(config.imgdir) / filename)
        img.thumbnail((1920, 1080))
        img.save(scaled_img_dir / filename)

    return send_from_directory(scaled_img_dir, filename)


if __name__ == "__main__":
    app.run()
