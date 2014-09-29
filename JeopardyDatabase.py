import sqlite3

def populate(entries):
   conn = sqlite3.connect('jeopardy.db')
   c = conn.cursor()
   _createTables(c)
   _insertValues(c, entries)
   conn.commit()
   conn.close()

def _createTables(c):
   c.execute("CREATE TABLE IF NOT EXISTS category (name VARCHAR PRIMARY KEY, round VARCHAR)")
   c.execute("CREATE TABLE IF NOT EXISTS question (question VARCHAR PRIMARY KEY, answer VARCHAR, category VARCHAR, FOREIGN KEY(category) REFERENCES category(name))")

def _insertValues(c, entries):
   for entry in entries:
      c.execute("INSERT OR IGNORE INTO category VALUES (?, ?)", (entry["category"], entry["round"]))
      c.execute("INSERT OR IGNORE INTO question VALUES (?, ?, ?)", (sqlite3.Binary(entry["question"]), sqlite3.Binary(entry["answer"]), entry["category"]))
