import secrets
import base64
import sqlite3
import io
from datetime import datetime as dt
from os.path import dirname, sep

conn = sqlite3.connect(f'{dirname(__file__ )}{sep}test.db')


def set_file(fp, mine: str, delete_date: dt = None) -> str:
    id = secrets.randbits(48)
    cur = conn.cursor()
    values = {
        'id': id, 'file': fp.read(),
        'update': dt.now().timestamp(), 'mine': mine}

    if delete_date is not None:
        values += {'deldate': delete_date.timestamp()}

    cur.execute('''
    INSERT INTO TREMS (id, file, upload_date, delete_date) VALUES(
      :id,
      :file,
      :update,
      :deldate
    );
    ''', values)
    conn.commit()
    return base64.urlsafe_b64encode(id.to_bytes(3, 'big'))


def get_file(id: str) -> tuple[io.BytesIO, str, str]:
    cur = conn.cursor()
    id = int.from_bytes(base64.urlsafe_b64decode(id), 'big')
    cur.execute('SELECT id FROM files')
    if id not in [x[0] for x in cur.fetchall()]:
        return None, None, None

    cur.execute('SELECT file, mine, file_name FROM files WHERE id = ?;', (id,))
    fp = cur.fetchall()[0]
    return (io.BytesIO(fp[0]),) + fp[1:]
