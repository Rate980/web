import secrets
import base64
import sqlite3
import io
from datetime import datetime as dt
from os.path import dirname, sep

conn = sqlite3.connect(f'{dirname(__file__ )}{sep}test.db')


def set_file(
        fp, mine: str, file_name: str = None, delete_date: dt = None) -> str:

    id = secrets.randbits(48)
    cur = conn.cursor()
    if file_name is None:
        try:
            file_name = fp.name
        except AttributeError:
            raise ValueError('file name is not found')
    values = {
        'id': id, 'file': fp.read(),
        'update': dt.now().timestamp(), 'mine': mine,
        'deldate': None, 'name': file_name}

    if delete_date is not None:
        values['deldate'] = delete_date.timestamp()

    cur.execute('''
    INSERT INTO files (
      id, file, upload_date, delete_date, mine, file_name)
    VALUES(
      :id,
      :file,
      :update,
      :deldate,
      :mine,
      :name
    );
    ''', values)
    conn.commit()
    return base64.urlsafe_b64encode(id.to_bytes(6, 'big')).decode('utf8')


def get_file(str_id: str) -> tuple[io.BytesIO, str, str]:
    cur = conn.cursor()
    byte_id = str_id.encord('utf8')
    id = int.from_bytes(base64.urlsafe_b64decode(byte_id), 'big')
    cur.execute('SELECT id FROM files')
    if id not in [x[0] for x in cur.fetchall()]:
        return None, None, None

    cur.execute('SELECT file, mine, file_name FROM files WHERE id = ?;', (id,))
    fp = cur.fetchall()[0]
    return (io.BytesIO(fp[0]),) + fp[1:]
