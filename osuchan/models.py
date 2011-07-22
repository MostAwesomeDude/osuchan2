import datetime

from flaskext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Wordfilter(db.Model):
    __tablename__ = "badwords"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    replacement = db.Column(db.String)

class Category(db.Model):
    __tablename__ = "boardcategory"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

class Board(db.Model):
    __tablename__ = "board"

    name = db.Column(db.String)
    abbreviation = db.Column(db.String, primary_key=True)
    category = db.Column(db.Integer, db.ForeignKey("boardcategory.id"))

    def __init__(self, abbreviation, name):
        self.abbreviation = abbreviation
        self.name = name

class Thread(db.Model):
    __tablename__ = "thread"

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String)
    author = db.Column(db.String)
    board = db.Column(db.String, db.ForeignKey("board.abbreviation"))

    def __init__(self, board, subject, author):
        self.board = board
        self.subject = subject
        self.author = author

class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, nullable=False)
    threadid = db.Column(db.Integer, db.ForeignKey("thread.id"), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    comment = db.Column(db.String)
    email = db.Column(db.String)
    file = db.Column(db.String)

    thread = db.relationship(Thread, backref="posts", single_parent=True,
        cascade="all, delete, delete-orphan")

    def __init__(self, author, comment, email, file):
        self.comment = comment
        self.author = author
        self.email = email
        self.file = file

        self.timestamp = datetime.datetime.now()

class File(db.Model):
    __tablename__ = "file"

    id = db.Column(db.Integer, primary_key=True)
    postid = db.Column(db.Integer, db.ForeignKey("post.id"))
    filename = db.Column(db.String, nullable=False)

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine("sqlite:///temp.db")
    db.Model.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()

    test = Board("test", "Test Board")
    session.add(test)
    session.commit()
