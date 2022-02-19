import os
import psycopg2

conn = psycopg2.connect(
	host="localhost",
	database="stories_db",
	user=os.environ['jennifermklein'],
	password=os.environ['dbpw'])

cur = conn.cursor()

curr.execute('DROP TABLE IF EXISTS words;')
curr.execute('CREATE TABLE stories (id serial PRIMARY KEY,
				date_time text,
				title text,
				content text);'
				)

conn.commit()

cur.close()
conn.close()

