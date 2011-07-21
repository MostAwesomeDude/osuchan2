#!/usr/bin/env python

if __name__ == "__main__":
    from osuchan import app
    app.run(debug=True, host="0.0.0.0", port=1337)

import hashlib
import mimetypes

import magic

from flask import Flask, render_template, request, url_for

app = Flask(__name__)

cookie = magic.open(magic.MAGIC_MIME)
cookie.load()

import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///test.db")
sm = sessionmaker(bind=engine)

header="OSUChan"

def save_file(f):
    """
    Save the given file resource to disk.

    Returns the filename on disk.
    """

    hash = hashlib.md5(f.file.read())
    f.file.seek(0)

    md5sum = hash.hexdigest()

    mime = cookie.buffer(f.file.read())
    f.file.seek(0)

    extension = mimetypes.guess_extension(mime.split(";")[0])

    filename = "%s%s" % (md5sum, extension)
    fh = open("static/images/%s" % filename, 'wb')
    fh.write(f.file.read())
    fh.close()

    return filename

@app.route('/')
def index():
    session = sm()
    boards = [(b.name, b.abbreviation) for b in session.query(models.Board)]
    return render_template("index.html", title=header, boards=boards)

@app.route('/<board>/comment', methods=('POST',))
def comment(board):
    email = request.form["email"]

    if not request.form['subject']:
        return "You forgot to fill out the subject"
    if not request.form['name']:
        return "You forgot to fill our your name"
    if not request.form['comment']:
        return "You forgot to fill in a comment!"
    if not email:
        return "You forgot to provide an email address"
    if "datafile" not in request.form:
        return "You forgot to select a file to upload"

    filename = save_file(request.form["datafile"])

    session = sm()

    # Create thread and first post, inserting them together.
    thread = models.Thread(board, request.form["subject"],
        request.form["name"])
    post = models.Post(request.form["name"], request.form["comment"],
        request.form["email"], filename)

    thread.posts = [post]

    session.add(thread)
    session.commit()

    if email == "noko":
        url = url_for("showthread", board=board, thread=thread.id)
    else:
        url = url_for("showboard", board=board)

    return render_template("redirect.html", url=url)

@app.route('/<board>/<thread>/comment', methods=('POST',))
def threadcomment(board, thread):
    email = request.form["email"]

    if not request.form['name']:
        return "You forgot to fill our your name"
    if not request.form['comment']:
        return "You forgot to fill in a comment!"
    if not email:
        return "You forgot to provide an email address"

    if "datafile" in request.form:
        filename = save_file(request.form["datafile"])
    else:
        filename = ""

    session = sm()

    post = models.Post(request.form["name"], request.form["comment"],
        request.form["email"], filename)
    post.threadid = thread

    session.add(post)
    session.commit()

    if email == "noko":
        url = url_for("showthread", board=board, thread=thread)
    else:
        url = url_for("showboard", board=board)

    return render_template("redirect.html", url=url)

@app.route('/<board>')
def showboard(board):
    session = sm()

    query = session.query(models.Thread).filter_by(board=board)
    threads = query.all()

    return render_template("showboard.html", title=board, board=board,
        threads=threads)

@app.route('/<board>/<thread>')
def showthread(board, thread):
    session = sm()

    query = session.query(models.Thread).filter_by(id=thread)
    subject = query.one().subject

    query = session.query(models.Post).filter_by(threadid=thread)
    query = query.order_by(models.Post.timestamp)
    posts = query.all()

    return render_template("showthread.html", title=subject, board=board,
        posts=posts, thread=thread)
