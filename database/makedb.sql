CREATE TABLE files(
  id INT primary key,
  file BLOB,
  mime TEXT,
  file_name TEXT,
  upload_date REAL,
  delete_date REAL
);
