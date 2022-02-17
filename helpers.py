
import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import sqlite3

# connect to database
def connect():
    return sqlite3.connect('test.db')

# query highest story id in table and assign to currStory
def get_current_story():
    cur = connect().cursor()
    return int(str(cur.execute('SELECT MAX(story_id) FROM words;').fetchall()[0])[1:-2])

# check if user session is the same as previously submitted word
def same_session():
    # connect to database
    db = connect()
    cur = db.cursor()

    last_session = str(cur.execute('SELECT session_id FROM words WHERE id=(SELECT MAX(id) FROM words);').fetchall()[0])[2:-3]

    return session.sid == last_session