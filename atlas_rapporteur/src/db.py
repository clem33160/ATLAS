import sqlite3
from .config import BASE

def init_db():
    p=BASE/'runtime/db/atlas.db'
    p.parent.mkdir(parents=True,exist_ok=True)
    con=sqlite3.connect(p)
    cur=con.cursor()
    cur.execute('create table if not exists leads(id integer primary key, url text, title text, score integer, tier text)')
    con.commit(); con.close()
