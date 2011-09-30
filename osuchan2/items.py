from axiom.item import Item
from axiom.attributes import integer, path, reference, text, timestamp

class Wordfilter(Item):
    typeName = "badwords"
    schemaVersion = 1

    name = text(allowNone=False)
    replacement = text(allowNone=False)

class Category(Item):
    typeName = "boardcategory"
    schemaVersion = 1

    title = text(allowNone=False)

class Board(Item):
    typeName = "board"
    schemaVersion = 1

    name = text()
    abbreviation = text(allowNone=False)
    category = reference()

class Thread(Item):
    typeName = "thread"
    schemaVersion = 1

    subject = text()
    board = reference()

class Post(Item):
    typeName = "post"
    schemaVersion = 1

    number = integer()
    author = text(allowNone=False)
    thread = reference(allowNone=False)
    timestamp = timestamp()
    comment = text()
    email = text()
    file = path()