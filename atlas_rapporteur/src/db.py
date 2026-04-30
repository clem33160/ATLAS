import sqlite3
from contextlib import contextmanager
from .config import BASE

DB_PATH = BASE / 'runtime/db/atlas.db'

@contextmanager
def get_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    try:
        yield con
    finally:
        con.commit(); con.close()


def init_db():
    with get_db() as con:
        cur = con.cursor()
        cur.executescript('''
        create table if not exists searches(id integer primary key, ts text default current_timestamp, query text, provider text, country text, trade text, city text, cost_eur real, useful_results integer default 0, rejected_results integer default 0);
        create table if not exists search_results(id integer primary key, search_id integer, url text, title text, snippet text, freshness_days integer, hash text);
        create table if not exists leads(id integer primary key, date text default current_timestamp, source_url text unique, title text, snippet text, extracted_text text, country text, city text, trade text, contact_phone text, contact_email text, contact_form text, lead_score integer, lead_category text, qualification_reasons text, rejection_reasons text, confidence real, status text default 'NEW');
        create table if not exists rejected_results(id integer primary key, url text, reason text, ts text default current_timestamp);
        create table if not exists budget_usage(id integer primary key, day text unique, queries integer, cost_eur real);
        create table if not exists query_performance(id integer primary key, query text unique, useful integer default 0, rejected integer default 0, disabled integer default 0);
        create table if not exists daily_reports(id integer primary key, day text unique, leads_count integer, rejected_count integer, budget_spent real, report_path text);
        ''')
