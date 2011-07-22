
import hashlib
import mimetypes

from flask import Blueprint, render_template, request, url_for

from osuchan.models import db, Board, Post, Thread

osuchan = Blueprint("osuchan", __name__, static_folder="static",
    template_folder="templates")

header = "OSUChan"

def save_file(f):
    """
    Save the given file resource to disk.

    Returns the filename on disk.
    """

    hash = hashlib.md5(f.stream.read())
    f.stream.seek(0)

    md5sum = hash.hexdigest()

    extension = mimetypes.guess_extension(f.mimetype)

    filename = "%s%s" % (md5sum, extension)
    f.save("static/images/%s" % filename)

    return filename

@osuchan.route('/')
def index():
    boards = [(b.name, b.abbreviation) for b in Board.query.all()]
    return render_template("index.html", title=header, boards=boards)

@osuchan.route('/<board>/comment', methods=('POST',))
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
    if "datafile" not in request.files:
        return "You forgot to select a file to upload"

    filename = save_file(request.files["datafile"])

    # Create thread and first post, inserting them together.
    thread = Thread(board, request.form["subject"],
        request.form["name"])
    post = Post(request.form["name"], request.form["comment"],
        request.form["email"], filename)

    thread.posts = [post]

    db.session.add(thread)
    db.session.commit()

    if email == "noko":
        url = url_for("showthread", board=board, thread=thread.id)
    else:
        url = url_for("showboard", board=board)

    return render_template("redirect.html", url=url)

@osuchan.route('/<board>/<int:thread>/comment', methods=('POST',))
def threadcomment(board, thread):
    email = request.form["email"]

    if not request.form['name']:
        return "You forgot to fill our your name"
    if not request.form['comment']:
        return "You forgot to fill in a comment!"
    if not email:
        return "You forgot to provide an email address"

    if "datafile" in request.file:
        filename = save_file(request.file["datafile"])
    else:
        filename = ""

    post = Post(request.form["name"], request.form["comment"],
        request.form["email"], filename)
    post.threadid = thread

    db.session.add(post)
    db.session.commit()

    if email == "noko":
        url = url_for("showthread", board=board, thread=thread)
    else:
        url = url_for("showboard", board=board)

    return render_template("redirect.html", url=url)

@osuchan.route('/<board>/')
def showboard(board):
    threads = Thread.query.filter_by(board=board).all()

    return render_template("showboard.html", title=board, board=board,
        threads=threads)

@osuchan.route('/<board>/<int:thread>')
def showthread(board, thread):
    subject = Thread.query.filter_by(id=thread).one().subject

    query = Post.query.filter_by(threadid=thread).order_by(Post.timestamp)
    posts = query.all()

    return render_template("showthread.html", title=subject, board=board,
        posts=posts, thread=thread)
