import os

import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import psycopg2
# import enchant

# connect to database
def connect():
    db = psycopg2.connect(os.environ['DATABASE_URL'])
    return db

# query highest story id in table and assign to currStory
def get_current_story_num():
    cur = connect().cursor()
    cur.execute('SELECT MAX(id) FROM stories;')
    max_story = cur.fetchall()[0][0]
    if (max_story):
        return max_story

    return 1

# check if user session is the same as previously submitted word
def same_session():
    cur = connect().cursor()

    cur.execute('SELECT session_id FROM words WHERE id=(SELECT MAX(id) FROM words);')
    last_session = cur.fetchall()
    if (last_session):
        return session.sid == last_session[0][0]

    return False

# return current story as a string
def get_current_story(story_num):
    # query current story from database
    cur = connect().cursor()
    cur.execute('SELECT word FROM words WHERE story_id=%s ORDER BY id;',(story_num,))
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
    if check_word and (not ' ' in check_word): #and (dictionary.check(check_word) or check_word.isnumeric()):
        cur.execute('INSERT INTO words (word,session_id,story_id) VALUES(%s,%s,%s);',(word,session.sid,story_num))
        db.commit()
        return True
    return False

# add story to database
def archive_story(story_num):

    # connect to database
    db = connect()
    cur = db.cursor()

    STORY = get_current_story(story_num)

    # insert story into story table and make a new blank story
    cur.execute('UPDATE stories SET date_time=%s, story_content=%s WHERE id=%s;',(datetime.datetime.now().strftime("%B %d, %Y"),STORY,story_num))
    cur.execute('INSERT INTO stories (date_time, title, story_content) VALUES (null, null, null);')
    # cur.execute('INSERT INTO stories (id) VALUES(%s);',(story_num+1,))
    db.commit()