# -*- coding:utf-8 -*-

from flask import (
    Flask,
    request, session, g,
    redirect, url_for,
    abort, render_template, flash
)

app = Flask(__name__)


@app.route('/')
def index():
    return """
<h1>Hello, CentOS + Nginx + uWSGI + Flask</h1>
"""


if __name__ == '__main__':
    app.run(debug=True)

