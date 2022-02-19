import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import sqlite3
import psycopg2
import datetime
# import enchant

# connect to database
def connect():
    db = psycopg2.connect(host='localhost',
                        database='postgres',
                        user=os.environ['DB_USERNAME'],
                        password=os.environ['DB_PASSWORD'])
    return db

# query highest story id in table and assign to currStory
def get_current_story_num():
    
    cur = connect().cursor()
    cur.execute('SELECT MAX(id) FROM stories;')#.fetchall()[0][0]
    max_story = cur.fetchall()[0][0]
    if (max_story):
        return max_story

    return 1

# check if user session is the same as previously submitted word
def same_session():
    db = connect()
    cur = db.cursor()

    cur.execute('SELECT session_id FROM words WHERE id=(SELECT MAX(id) FROM words);')
    last_session = cur.fetchall()
    if (last_session):
        # last_session = last_session[0][0]
        return session.sid == last_session[0][0]

    return False

# return current story as a string
def get_current_story(story_num):
    # query current story from database
    cur = connect().cursor()
    cur.execute('SELECT word FROM words WHERE story_id=%s;',(story_num,))
    words_from_db = cur.fetchall()

    # create string from queried words
    words = []
    for word in words_from_db:
        words.append(word[0])
    story = ' '.join(words)

    return story


# add word to database, return false if word rejected
def insert_word(word, story_num):
    if not word:
        return False
    
    db = connect()
    cur = db.cursor()
    # dictionary = enchant.Dict("en_US")

    check_word = word.strip(' .,?:;-"!')
    if check_word: #and (dictionary.check(check_word) or check_word.isnumeric()):
        cur.execute('INSERT INTO words (word,session_id,story_id) VALUES(%s,%s,%s);',(word,session.sid,story_num))
        db.commit()
        return True
    return False

# add story to database
def archive_story(story_num):

    # connect to database
    db = connect()
    cur = db.cursor()

    # format story into string
    cur.execute('SELECT word FROM words WHERE story_id=%s;',(str(story_num),))
    words_from_db = cur.fetchall()
    words = []
    for word in words_from_db:
        words.append(word[0])
    STORY = ' '.join(words)

    # insert story into story table and make a new blank story
    cur.execute('UPDATE stories SET date_time=%s, story_content=%s WHERE id=%s;',(datetime.datetime.now(),STORY,story_num))
    cur.execute('INSERT INTO stories (id) VALUES(%s);',(story_num+1,))
    db.commit()