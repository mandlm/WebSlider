#!/usr/bin/python3

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello slider"

if __name__ == "__main__":
    app.run()
