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
        file = flask.request.files['uploadFile']
        id = db.set_file(file, fp_read=file.read())
        return flask.render_template(
            'uploader/upload.html.j2', id=id,
            server_name=flask.request.url_root)


@app.route('/download/<id>')
def download(id):
    fp = db.get_file(id)
    if fp[0] is None:
        return flask.abort(404)
    else:
        return (flask.send_file(
            fp[0], mimetype=fp[1], as_attachment=True,
            attachment_filename=fp[2])
        )
