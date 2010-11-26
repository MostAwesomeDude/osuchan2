#!/usr/bin/env python

from bottle import request, route, run, template, view
import bottle
bottle.debug(True)
import hashlib

DSN="dbname=cs440"
header="OSUChan"

import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///test.db")
sm = sessionmaker(bind=engine)

@route('/')
@view('index')
def index():
    session = sm()
    boards = [(b.name, b.abbreviation) for b in session.query(models.Board)]
    return {"title": header, "boards": boards}

@route('/static/:name')
def style(name):
    bottle.send_file(name,root='static')

@route('/static/images/:image')
def sendimage(image):
    bottle.send_file(image,root='static/images')

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

    datafile = request.POST['datafile']
    hash = hashlib.md5(datafile.file.read())
    md5sum = hash.hexdigest()
    datafile.file.seek(0)

    fh = open('static/images/%s' % md5sum, 'w')
    fh.write(datafile.file.read())
    fh.close()

    session = sm()

    # Insert thread entry
    thread = models.Thread(board, request.POST["subject"],
        request.POST["name"])
    session.add(thread)
    session.commit()

    threadid = thread.id
    
    # Insert first post
    post = models.Post(threadid, request.POST["comment"],
        request.POST["name"], request.POST["email"])
    session.add(post)
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

    datafile = request.POST.get('datafile')
    hash = hashlib.md5()
    hash.update(datafile.file.read())
    md5sum = hash.hexdigest()
    datafile.file.seek(0)

    fh = open('/home/bkero/cs440/static/images/%s' % md5sum, 'w')
    fh.write(datafile.file.read())
    fh.close()

    session = sm()

    post = models.Post(thread, request.POST["name"], request.POST["comment"],
    request.POST["email"], md5sum)
    session.add(post)
    session.commit()

    return "<html><head><meta http-equiv='refresh' content='3;url=http://ponderosa.osuosl.org:1337/%s/%s'></head><body>Message Posted!  Please wait 3 seconds to be redirected back to the thread.</body></html>" % (board, thread)

@route('/:board')
@view('showboard')
def showboard(board):
    session = sm()

    threads = []
    query = session.query(models.Thread)
    for thread in query.filter(models.Thread.board==board):
        threads.append((thread.id, thread.subject, thread.author))

    return dict(title=board, board=board, threads=threads)

@route('/:board/:thread')
@view('showthread')
def showthread(board, thread):
    session = sm()

    query = session.query(models.Thread).filter(models.Thread.id==thread)
    subject = query.one().subject

    query = session.query(models.Post).filter(models.Post.threadid==thread)
    query = query.order_by(models.Post.timestamp)
    posts = []
    for post in query:
        posts.append((post.id, post.author, post.threadid, post.timestamp,
        post.comment, post.email, post.file))

    return dict(title=subject, board=board, posts=posts, thread=thread)

run(host='0.0.0.0', port=1337)
