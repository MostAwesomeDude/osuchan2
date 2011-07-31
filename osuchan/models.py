import datetime

from flaskext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Wordfilter(db.Model):
    __tablename__ = "badwords"

    name = db.Column(db.Unicode(30), primary_key=True)
    replacement = db.Column(db.Unicode(30))

class Category(db.Model):
    __tablename__ = "boardcategory"

    title = db.Column(db.Unicode(30), primary_key=True)

class Board(db.Model):
    __tablename__ = "board"

    name = db.Column(db.Unicode(30))
    abbreviation = db.Column(db.String(5), primary_key=True)
    category = db.Column(db.Unicode(30), db.ForeignKey(Category.title))

    def __init__(self, abbreviation, name):
        self.abbreviation = abbreviation
        self.name = name

class Thread(db.Model):
    __tablename__ = "thread"

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.Unicode(50))
    author = db.Column(db.Unicode(30))
    board = db.Column(db.String(5), db.ForeignKey(Board.abbreviation))

    def __init__(self, board, subject, author):
        self.board = board
        self.subject = subject
        self.author = author

class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Unicode(30), nullable=False)
    threadid = db.Column(db.Integer, db.ForeignKey(Thread.id), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    comment = db.Column(db.UnicodeText(1024*1024))
    email = db.Column(db.String(30))
    file = db.Column(db.String(50))

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

    postid = db.Column(db.Integer, db.ForeignKey(Post.id))
    filename = db.Column(db.String(50), primary_key=True)

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine("sqlite:///temp.db")
    db.Model.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()

    test = Board("test", "Test Board")
    session.add(test)
    session.commit()
