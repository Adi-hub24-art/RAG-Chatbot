import sqlite3
from chunks import chunk
from embeddings import model

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS notes (" \
"            id INTEGER PRIMARY KEY AUTOINCREMENT," \
"            source TEXT,"\
"            chunk_index INTEGER,"\
"            body TEXT NOT NULL," \
"            embedding BLOB)")

for piece in chunk(100):
    cur.execute("INSERT INTO notes (source, body, embedding) VALUES (?, ?, ?)", ("aditya_profile.txt", piece, model(piece)))

conn.commit()
conn.close()
