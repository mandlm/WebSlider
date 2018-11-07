#!/usr/bin/python3

from flask import Flask, render_template, send_from_directory, redirect, url_for
from random import choice
from pathlib import Path
from PIL import Image
from time import time

import config

app = Flask(__name__)


@app.route("/")
def random():
    return render_template("random.html", refresh=config.refresh)


@app.route("/random_image/")
def random_image():
    imgdir = Path(config.imgdir)
    last_modified_time, last_modified_file = max(
        (f.stat().st_mtime, f) for f in imgdir.glob("*.jpg")
    )

    if time() - last_modified_time <= 60:
        selected_image = last_modified_file.relative_to(imgdir)
    else:
        images = list(imgdir.glob("*.jpg"))
        selected_image = choice(images).relative_to(imgdir)

    return redirect(url_for("image", filename=selected_image))


@app.route("/img/<path:filename>")
def image(filename):
    scaled_img_dir = Path(config.imgdir) / ".slider" / "fhd"

    if not scaled_img_dir.exists():
        scaled_img_dir.mkdir(parents=True)

    if not (scaled_img_dir / filename).exists():
        img = Image.open(Path(config.imgdir) / filename)
        img.thumbnail((1920, 1080))
        img.save(scaled_img_dir / filename)

    return send_from_directory(scaled_img_dir, filename)


if __name__ == "__main__":
    app.run()
