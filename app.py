import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from helpers import connect, get_current_story, get_current_story_num, same_session, insert_word, archive_story

# configure app
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# home page showing current story. user can submit new word or end the story
@app.route('/', methods=["GET","POST"])
def index():

    curr_story = get_current_story_num()
    db = connect()
    cur = db.cursor()

    if request.method == "POST":

        # reject if same user takes more than one action in a row
        if same_session():
            return redirect("/")

        # if word submitted, verify validity and add to database
        if (insert_word(request.form.get("add_word"),curr_story)):
            return redirect("/")
        
        # start new story
        if request.form.get("end_story") and get_current_story(curr_story):
            archive_story(curr_story)
            return redirect("/title")

        return redirect("/")

    return render_template('index.html', story=get_current_story(curr_story))

@app.route('/story', methods=["GET"])
def story():
    # Get the current story from the database
    return get_current_story(get_current_story_num())

@app.route('/session_error', methods=["GET","POST"])
def session_error():
    return str(same_session())

# page displaying previous stories
@app.route('/archive', methods=["GET","POST"])
def archive():

    cur = connect().cursor()

    # create dictionary from query of previous stories
    cur.execute('SELECT * FROM stories WHERE id!=(SELECT MAX(id) FROM stories)')
    stories_from_db = cur.fetchall()
    archived_stories = {}
    for row in stories_from_db:
        archived_stories[row[3]] = {'datetime': row[1],'title': row[2], 'content': row[3]}

    return render_template('archive.html',stories=archived_stories)

# add title after ending a story
@app.route('/title', methods=["GET","POST"])
def title():

    db = connect()
    cur = db.cursor()
    title_story = get_current_story_num()-1

    if request.method == "POST":
        # add title to stories database
        if request.form.get("add_title"):
            cur.execute('UPDATE stories SET title=%s WHERE id=%s;',(request.form.get("add_title"),title_story))
            db.commit()

        return redirect("/archive")

    return render_template('title.html', story=get_current_story(title_story))

# about page
@app.route('/about', methods=["GET"])
def about():
    return render_template('about.html')

    