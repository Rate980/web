#!/usr/bin/env python3

import flask
import database as db

app = flask.Blueprint('uploader', __name__)


@app.route('/')
def uproder_index():

    return flask.render_template('uploader/index.html.j2')


@app.route('/upload', methods=['POST'])
def upload():
    print(flask.request.files['uploadFile'])
    if flask.request.files:
        id = db.set_file(flask.request.files[uploadFile])
        return flask.render_template(id=id, server_name=flask.request.url_root)


@app.route('/download/<id>')
def download(id):
