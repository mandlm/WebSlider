#!/usr/bin/python3

from flask import (
    Flask,
    render_template,
    send_from_directory,
    redirect,
    url_for,
    request,
)
from random import choice
from pathlib import Path
from PIL import Image
from time import time
from hashlib import sha256
import click
from shutil import rmtree
from tempfile import gettempdir

import config

app = Flask(__name__)

imgdir = Path(config.imgdir).expanduser().resolve()
cache_resolution = config.resolution
cache_dir = (
    Path(gettempdir()) / "webslider"
    if config.cachedir == "auto"
    else Path(config.cachedir)
) / ("%sx%s" % cache_resolution)


def find_images():
    images = set()
    for filetype in config.filetypes:
        glob = "**/" + filetype if config.recursive else filetype
        images.update(imgdir.glob(glob))
    return list(images)


@app.route("/")
def random():
    print(request.remote_addr, request.base_url)
    return render_template("random.html", refresh=config.refresh)


@app.route("/random_image/")
def random_image():
    print(request.remote_addr, request.base_url)
    try:
        last_modified_time, last_modified_file = max(
            (f.stat().st_mtime, f) for f in find_images()
        )

        if time() - last_modified_time <= 60:
            selected_image = last_modified_file.relative_to(imgdir)
        else:
            images = find_images()
            selected_image = choice(images).relative_to(imgdir)
    except ValueError:
        return redirect(url_for("static", filename="clear.gif"))

    return redirect(
        url_for("image", filename=selected_image)
        + "?hash=%s" % get_cache_filename(selected_image)
    )


@app.route("/img/<path:filename>")
def image(filename):
    print(request.remote_addr, request.base_url)
    cache_filename = create_cache_file(filename)

    return send_from_directory(cache_dir, cache_filename)


def rm_cachedir():
    if cache_dir.exists():
        print("Removing cache dir", cache_dir)
        rmtree(cache_dir)


def create_cachedir():
    if not cache_dir.exists():
        print("Creating cache dir", cache_dir)
        cache_dir.mkdir(parents=True)


def create_cache_file(filename):
    create_cachedir()
    cache_file = get_cache_filename(filename)

    if not (cache_dir / cache_file).exists():
        print("Creating cache file", filename)
        img = Image.open(imgdir / filename)
        img.thumbnail(cache_resolution)
        img.save(cache_dir / cache_file, "JPEG")

    return cache_file


def get_cache_filename(filename):
    original_file_path = imgdir / filename
    return sha256(str(original_file_path.resolve()).encode("utf-8")).hexdigest()


def pre_cache_images():
    for image_file in sorted(find_images()):
        create_cache_file(image_file.relative_to(imgdir))


@click.command()
@click.option("--build-cache", is_flag=True, default=False, help="pre-cache images")
@click.option(
    "--clear-cache", is_flag=True, default=False, help="clear cache directory"
)
def run_slider(build_cache, clear_cache):
    if clear_cache:
        rm_cachedir()
    if build_cache:
        pre_cache_images()

    app.run(host="0.0.0.0")


if __name__ == "__main__":
    run_slider()
