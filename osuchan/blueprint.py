
import hashlib
import mimetypes

from flask import Blueprint, render_template, request, url_for

from osuchan.forms import ChanForm
from osuchan.models import db, Board, Post, Thread

osuchan = Blueprint("osuchan", __name__, static_folder="static",
    template_folder="templates")

header = "OSUChan"

def save_file(f):
    """
    Save the given file resource to disk.

    Returns the filename on disk.
    """

    # Empty file?
    if not f.content_length:
        return ""

    hash = hashlib.md5(f.stream.read())
    f.stream.seek(0)

    md5sum = hash.hexdigest()

    extension = mimetypes.guess_extension(f.content_type)

    filename = "%s%s" % (md5sum, extension)
    f.save("static/images/%s" % filename)

    return filename

@osuchan.route('/')
def index():
    boards = [(b.name, b.abbreviation) for b in Board.query.all()]
    return render_template("oc/index.html", title=header, boards=boards)

@osuchan.route('/<board>/comment', methods=('POST',))
def comment(board):
    form = ChanForm()

    if not form.validate_on_submit():
        return "Error"

    if "datafile" not in request.files:
        return "You forgot to select a file to upload"

    filename = save_file(request.files["datafile"])

    # Create thread and first post, inserting them together.
    thread = Thread(board, form.subject.data, form.name.data)
    post = Post(form.name.data, form.comment.data, form.email.data, filename)

    thread.posts = [post]

    db.session.add(thread)
    db.session.commit()

    email = form.email.data

    if email == "noko":
        if request.referrer:
            url = request.referrer
        else:
            url = url_for("osuchan.showthread", board=board, tid=thread)
    else:
        url = url_for("osuchan.showboard", board=board)

    return render_template("oc/redirect.html", url=url)

@osuchan.route('/<board>/<int:thread>/comment', methods=('POST',))
def threadcomment(board, thread):
    form = ChanForm()

    if not form.validate_on_submit():
        return "Error"

    if "datafile" in request.files:
        filename = save_file(request.files["datafile"])
    else:
        filename = ""

    post = Post(form.name.data, form.comment.data, form.email.data, filename)
    post.threadid = thread

    db.session.add(post)
    db.session.commit()

    email = form.email.data

    if email == "noko":
        if request.referrer:
            url = request.referrer
        else:
            url = url_for("osuchan.showthread", board=board, tid=thread)
    else:
        url = url_for("osuchan.showboard", board=board)

    return render_template("oc/redirect.html", url=url)

@osuchan.route('/<board>/')
def showboard(board):
    form = ChanForm()
    threads = Thread.query.filter_by(board=board).all()

    return render_template("oc/showboard.html", title=board, board=board,
        threads=threads, form=form)

@osuchan.route('/<board>/<int:tid>')
def showthread(board, tid):
    form = ChanForm()
    thread = Thread.query.filter_by(id=tid).one()
    subject = thread.subject

    query = Post.query.filter_by(threadid=tid).order_by(Post.timestamp)
    posts = query.all()

    return render_template("oc/showthread.html", title=subject, board=board,
        posts=posts, thread=thread, form=form)
