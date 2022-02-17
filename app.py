import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import sqlite3
import enchant
from helpers import connect, get_current_story, same_session

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# global vars
currStory = get_current_story()
dictionary = enchant.Dict("en_US")

# add story to database
def archive_story(story_num):
    thisStory = story_num # replace with currStory here and below

    # connect to database
    db = connect()
    cur = db.cursor()

    # format story into string
    words_from_db = cur.execute('SELECT word FROM words WHERE story_id=?;',(str(thisStory),)).fetchall()
    words = []
    for word in words_from_db:
        words.append(str(word)[2:-3])
    STORY = ' '.join(words)

    # insert story into story table
    cur.execute('INSERT INTO stories (title,story_content) VALUES(?,?);',('Title',STORY))
    db.commit()

# home page where user can see current story, submit new word, and end the story
@app.route('/', methods=["GET","POST"])
def index():

    global currStory
    global dictionary

    # connect to database
    db = connect()
    cur = db.cursor()

    if request.method == "POST":

        # reject if same user takes more than one action in a row
        if same_session():
            # add error message?
            return redirect("/")

        # if word submitted, verify validity and add to database
        if request.form.get("add_word"):
            NEW_WORD = request.form.get("add_word").strip()
            check_word = NEW_WORD.strip('.,?:;-"')
            if check_word and (dictionary.check(check_word) or check_word.isnumeric()):
                cur.execute('INSERT INTO words (word,session_id,story_id) VALUES(?,?,?);',(NEW_WORD,session.sid,currStory))
                db.commit()
                return redirect("/")
        
        # start new story
        if request.form.get("end_story"):
            archive_story(currStory)
            currStory += 1
            return redirect("/archive")

        return redirect("/")

    # query current story from database
    words_from_db = cur.execute('SELECT word FROM words WHERE story_id=?;',(str(currStory),)).fetchall()

    # create string from queried words
    words = []
    for word in words_from_db:
        words.append(str(word)[2:-3])
    STORY = ' '.join(words)

    return render_template('index.html', story=STORY)

# page displaying previous stories
@app.route('/archive', methods=["GET","POST"])
def archive():

    cur = connect().cursor()
    global currStory

    # create dictionary from query of previous stories
    archived_stories = {}
    for story in range(currStory-1,0,-1):
        testwords = cur.execute('SELECT word FROM words WHERE story_id=?;',(str(story),)).fetchall()
        archived_stories[story] = []
        for word in testwords:
            archived_stories[story].append(str(word)[2:-3])

    return render_template('archive.html',stories=archived_stories)
