import sqlite3

def populate(entries):
   conn = sqlite3.connect('jeopardy.db')
   c = conn.cursor()
   c.execute("CREATE TABLE IF NOT EXISTS jeopardy (round, category, question, answer)")
   for entry in entries:
      c.execute("INSERT INTO jeopardy VALUES ( ?, ?, ?, ?)", (entry["round"], entry["category"], sqlite3.Binary(entry["question"]), sqlite3.Binary(entry["answer"])))
   conn.commit()
   conn.close()
