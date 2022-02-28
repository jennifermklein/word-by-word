import os
import psycopg2

db = psycopg2.connect(
	host="localhost",
	database="stories_db",
	user=os.environ['jennifermklein'],
	password=os.environ['dbpw'])

cur = db.cursor()

cur.execute('DROP TABLE IF EXISTS words;')
cur.execute('CREATE TABLE stories (id SERIAL PRIMARY KEY, date_time TEXT, title TEXT, story_content TEXT);')
cur.execute('CREATE TABLE words (id SERIAL PRIMARY KEY, word TEXT NOT NULL, session_id TEXT, story_id INTEGER REFERENCES stories(id));')
cur.execute('INSERT INTO stories (date_time, title, story_content) VALUES (null, null, null);')

db.commit()

cur.close()
db.close()

