import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import sqlite3
import enchant
from helpers import connect, get_current_story, get_current_story_num, same_session, archive_story

# configure app
app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# global vars
currStory = get_current_story_num()
dictionary = enchant.Dict("en_US")

# home page showing current story. user can submit new word or end the story
@app.route('/', methods=["GET","POST"])
def index():

    global currStory
    global dictionary
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
            check_word = NEW_WORD.strip('.,?:;-"!')
            if check_word and (dictionary.check(check_word) or check_word.isnumeric()):
                cur.execute('INSERT INTO words (word,session_id,story_id) VALUES(?,?,?);',(NEW_WORD,session.sid,currStory))
                db.commit()
                return redirect("/")
        
        # start new story
        if request.form.get("end_story") and get_current_story(currStory):
            archive_story(currStory)
            currStory += 1
            return redirect("/title")

        return redirect("/")

    return render_template('index.html', story=get_current_story(currStory))

@app.route('/story', methods=["GET"])
def story():
    # Get the current story from the database
    return get_current_story(currStory)

# page displaying previous stories
@app.route('/archive', methods=["GET","POST"])
def archive():

    cur = connect().cursor()
    global currStory

    # create dictionary from query of previous stories
    stories_from_db = cur.execute('SELECT * FROM stories').fetchall()
    archived_stories = {}
    for row in stories_from_db:
        archived_stories[row[3]] = {'title': row[1], 'content': row[2]}

    return render_template('archive.html',stories=archived_stories)

# page to add title after ending a story
@app.route('/title', methods=["GET","POST"])
def title():

    global currStory
    db = connect()
    cur = db.cursor()

    if request.method == "POST":
        # add title to stories database
        if request.form.get("add_title"):
            cur.execute('UPDATE stories SET title=? WHERE id=?;',(request.form.get("add_title"),currStory-1))
            db.commit()

        return redirect("/archive")

    return render_template('title.html', story=get_current_story(currStory-1))

# about page
@app.route('/about', methods=["GET"])
def about():
    return render_template('about.html')

    