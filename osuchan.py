#!/usr/bin/env python

import hashlib
import mimetypes

import magic

cookie = magic.open(magic.MAGIC_MIME)
cookie.load()

from bottle import debug, request, route, run, send_file, view
debug(True)

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

@route('/')
@view('index')
def index():
    session = sm()
    boards = [(b.name, b.abbreviation) for b in session.query(models.Board)]
    return {"title": header, "boards": boards}

@route('/static/:name')
def style(name):
    send_file(name,root='static')

@route('/static/images/:image')
def sendimage(image):
    send_file(image,root='static/images')

@route('/:board/comment', method='POST')
def comment(board):

    if not request.POST['subject']:
        return "You forgot to fill out the subject"
    if not request.POST['name']:
        return "You forgot to fill our your name"
    if not request.POST['comment']:
        return "You forgot to fill in a comment!"
    if not request.POST['email']:
        return "You forgot to provide an email address"
    if "datafile" not in request.POST:
        return "You forgot to select a file to upload"

    filename = save_file(request.POST["datafile"])

    session = sm()

    # Create thread and first post, inserting them together.
    thread = models.Thread(board, request.POST["subject"],
        request.POST["name"])
    post = models.Post(request.POST["comment"], request.POST["name"],
        request.POST["email"], filename)

    thread.posts = [post]

    session.add(thread)
    session.commit()
    
    return "<html><head><meta http-equiv='refresh' content='3;url=http://ponderosa.osuosl.org:1337/%s'></head><body>Message Posted!  Please wait 3 seconds to be redirected back to the board index.</body></html>" % board

@route('/:board/:thread/comment', method='POST')
def threadcomment(board, thread):

    if not request.POST['name']:
        return "You forgot to fill our your name"
    if not request.POST['comment']:
        return "You forgot to fill in a comment!"
    if not request.POST['email']:
        return "You forgot to provide an email address"

    if "datafile" in request.POST:
        filename = save_file(request.POST["datafile"])
    else:
        filename = ""

    session = sm()

    post = models.Post(request.POST["name"], request.POST["comment"],
        request.POST["email"], filename)
    post.threadid = thread

    session.add(post)
    session.commit()

    return "<html><head><meta http-equiv='refresh' content='3;url=http://ponderosa.osuosl.org:1337/%s/%s'></head><body>Message Posted!  Please wait 3 seconds to be redirected back to the thread.</body></html>" % (board, thread)

@route('/:board')
@view('showboard')
def showboard(board):
    session = sm()

    query = session.query(models.Thread).filter(models.Thread.board==board)
    threads = query.all()

    return dict(title=board, board=board, threads=threads)

@route('/:board/:thread')
@view('showthread')
def showthread(board, thread):
    session = sm()

    query = session.query(models.Thread).filter(models.Thread.id==thread)
    subject = query.one().subject

    query = session.query(models.Post).filter(models.Post.threadid==thread)
    query = query.order_by(models.Post.timestamp)
    posts = query.all()

    return dict(title=subject, board=board, posts=posts, thread=thread)

run(host='0.0.0.0', port=1337)
