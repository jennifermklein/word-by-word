
import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import sqlite3
import enchant

# connect to database
def connect():
    return sqlite3.connect('test.db')

# query highest story id in table and assign to currStory
def get_current_story_num():
    
    cur = connect().cursor()
    max_story = cur.execute('SELECT MAX(story_id) FROM stories;').fetchall()[0][0]

    if (max_story):
        max_story = max_story + 1
        return max_story

    return 1

# return current story as a string
def get_current_story(story_num):
    # query current story from database
    cur = connect().cursor()
    words_from_db = cur.execute('SELECT word FROM words WHERE story_id=?;',(story_num,)).fetchall()

    # create string from queried words
    words = []
    for word in words_from_db:
        words.append(word[0])
    story = ' '.join(words)

    return story

# check if user session is the same as previously submitted word
def same_session():
    db = connect()
    cur = db.cursor()

    last_session = cur.execute('SELECT session_id FROM words WHERE id=(SELECT MAX(id) FROM words);').fetchall()
    if (last_session):
        last_session = last_session[0][0]
        return session.sid == last_session

    return False

# add word to database, return false if word rejected
def insert_word(word, story_num):
    if not word:
        return False
    
    db = connect()
    cur = db.cursor()
    dictionary = enchant.Dict("en_US")

    check_word = word.strip(' .,?:;-"!')
    if check_word and (dictionary.check(check_word) or check_word.isnumeric()):
        cur.execute('INSERT INTO words (word,session_id,story_id) VALUES(?,?,?);',(word,session.sid,story_num))
        db.commit()
        return True
    return False

# add story to database
def archive_story(story_num):

    # connect to database
    db = connect()
    cur = db.cursor()

    # format story into string
    words_from_db = cur.execute('SELECT word FROM words WHERE story_id=?;',(str(story_num),)).fetchall()
    words = []
    for word in words_from_db:
        words.append(str(word)[2:-3])
    STORY = ' '.join(words)

    # insert story into story table
    cur.execute('INSERT INTO stories (story_content,story_id) VALUES(?,?);',(STORY,story_num))
    db.commit()