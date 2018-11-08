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
    img_glob = "*jpg"
    imgdir = Path(config.imgdir)
    last_modified_time, last_modified_file = max(
        (f.stat().st_mtime, f) for f in imgdir.glob(img_glob)
    )

    if time() - last_modified_time <= 60:
        selected_image = last_modified_file.relative_to(imgdir)
    else:
        images = list(imgdir.glob(img_glob))
        selected_image = choice(images).relative_to(imgdir)

    return redirect(url_for("image", filename=selected_image))


@app.route("/img/<path:filename>")
def image(filename):
    cache_resolution = (1920, 1080)
    cache_dir = Path(config.cachedir) / ("%sx%s" % cache_resolution)

    if not cache_dir.exists():
        cache_dir.mkdir(parents=True)

    if not (cache_dir / filename).exists():
        img = Image.open(Path(config.imgdir) / filename)
        img.thumbnail(cache_resolution)
        img.save(cache_dir / filename)

    return send_from_directory(cache_dir, filename)


if __name__ == "__main__":
    app.run()
