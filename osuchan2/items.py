from axiom.item import Item
from axiom.attributes import integer, path, reference, text, timestamp

from twisted.web.template import tags

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

    def tags(self, tag):
        return tag("/", tags.a(self.abbreviation, href=self.abbreviation),
            "/ - %s" % self.name)

class Thread(Item):
    typeName = "thread"
    schemaVersion = 1

    subject = text()
    board = reference()

    def tags(self, tag):
        first = self.store.findFirst(Post, Post.thread == self)
        if first is None:
            return tag(u"Empty thread")
        else:
            subject = u"%s - %s [" % (first.author, self.subject)
            link = tags.a("Reply", href="#")
            return tag(subject, link, "]")

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
