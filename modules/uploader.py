#!/usr/bin/env python3

import flask

app = flask.Blueprint('uploader', __name__)


@app.route('/')
def uproder_index():

    return flask.render_template('uploader/index.html.j2')
