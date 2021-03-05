import secrets
import base64
import sqlite3
import io
import mimetypes
from datetime import datetime as dt
from os.path import dirname, sep

import magic

dbname = f'{dirname(__file__ )}{sep}test.db'


def set_file(
        fp, file_name: str = None,
        delete_date: dt = None, fp_read: bytes = None) -> str:

    id = secrets.randbits(48)
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    read = fp.read()
    if read == b'':
        if fp_read is not None:
            read = fp_read
        else:
            raise ValueError('file bytes is not found, buffer may be flushed')
    if file_name is None:
        try:
            file_name = fp.filename
        except AttributeError:
            try:
                file_name = fp.name
            except AttributeError:
                raise ValueError('file name is not found')
    mime = magic.from_buffer(read, mime=True)
    name_mime = mimetypes.guess_type(file_name)[0]
    if name_mime is None:
        try:
            name_mime = fp.mimetype
        except AttributeError:
            name_mime = 'application/octet-stream'

    if ((name_mime is None and mime != 'application/octet-stream') or
            (mime != name_mime and mime != 'text/plain'
             and name_mime != 'application/octet-stream')):
        no_ext = '.'.join(file_name.split('.')[:-1])
        ext = mimetypes.guess_extension(mime)
        print(name_mime, mime)
        file_name = no_ext + ext

    if mime == 'text/plain':
        try:
            mime = fp.mimetype
        except AttributeError:
            mime = name_mime

    values = {
        'id': id, 'file': read,
        'update': dt.now().timestamp(), 'mime': mime,
        'deldate': None, 'name': file_name}

    if delete_date is not None:
        values['deldate'] = delete_date.timestamp()

    cur.execute('''
    INSERT INTO files (
      id, file, upload_date, delete_date, mime, file_name)
    VALUES(
      :id,
      :file,
      :update,
      :deldate,
      :mime,
      :name
    );
    ''', values)
    conn.commit()
    return base64.urlsafe_b64encode(id.to_bytes(6, 'big')).decode('utf8')


def get_file(str_id: str) -> tuple[io.BytesIO, str, str]:
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    byte_id = str_id.encode('utf8')
    id = int.from_bytes(base64.urlsafe_b64decode(byte_id), 'big')
    cur.execute('SELECT id FROM files')
    if id not in [x[0] for x in cur.fetchall()]:
        raise ValueError(f'id "{id}" is not found in database')

    cur.execute('SELECT file, mime, file_name FROM files WHERE id = ?;', (id,))
    fp = cur.fetchall()[0]
    return (io.BytesIO(fp[0]),) + fp[1:]
