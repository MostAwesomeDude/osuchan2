import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Wordfilter(Base):
    __tablename__ = "badwords"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    replacement = Column(String)

class Category(Base):
    __tablename__ = "boardcategory"

    id = Column(Integer, primary_key=True)
    title = Column(String)

class Board(Base):
    __tablename__ = "board"

    name = Column(String)
    abbreviation = Column(String, primary_key=True)
    category = Column(Integer, ForeignKey("boardcategory.id"))

    def __init__(self, abbreviation, name):
        self.abbreviation = abbreviation
        self.name = name

class Thread(Base):
    __tablename__ = "thread"

    id = Column(Integer, primary_key=True)
    subject = Column(String)
    author = Column(String)
    board = Column(String, ForeignKey("board.abbreviation"))

    def __init__(self, board, subject, author):
        self.board = board
        self.subject = subject
        self.author = author

class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    author = Column(String, nullable=False)
    threadid = Column(Integer, ForeignKey("thread.id"))
    timestamp = Column(DateTime)
    comment = Column(String)
    email = Column(String)
    file = Column(String, nullable=True)

    def __init__(self, threadid, comment, author, email, file):
        self.threadid = threadid
        self.comment = comment
        self.author = author
        self.email = email
        self.file = file

        self.timestamp = datetime.datetime.now()

class File(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True)
    postid = Column(Integer, ForeignKey("post.id"))
    filename = Column(String, nullable=False)

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine("sqlite:///test.db")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()

    test = Board("test", "Test Board")
    session.add(test)
    session.commit()
