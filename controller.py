#!/usr/bin/env python3

import flask
import sys
import sass
import io
from modules import uploader

app = flask.Flask(__name__)
print(*sys.path, sep='\n')


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/ip')
def ip():
    return flask.request.remote_addr


@app.route('/test')
def test():
    return flask.render_template('test.html.j2')


@app.route('/sass')
def get_sass():
    file_name = flask.request.args.get('file')
    if app.debug:
        style = 'expanded'
        map = True
    else:
        style = 'compressed'
        map = False
    compiled_sass = sass.compile(
        filename=f'aseets/scss/{file_name}',
        output_style=style,
        source_map_embed=map
    )

    return flask.send_file(
        io.BytesIO(compiled_sass.encode('utf8')),
        mimetype='text/css')


@app.template_filter('sass')
def url_sass(name):
    return f'/sass?file={name}'


if __name__ == '__main__':
    app.register_blueprint(uploader.app, url_prefix='/uploader')
    app.run(debug=True)
