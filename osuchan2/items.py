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
            header = tags.header(subject, link, "]")

            post = first.tags(tags.div)

            # Retrieve posts and reverse them twice, to avoid having to get
            # the length of the table.
            others = self.store.query(Post, Post.thread == self, limit=4,
                sort=Post.timestamp.descending)
            posts = [p.tags(tags.div) for p in others]
            posts.reverse()

            return tag(header, post, *posts)

class Post(Item):
    typeName = "post"
    schemaVersion = 1

    number = integer(allowNone=False)
    author = text(allowNone=False)
    thread = reference(allowNone=False)
    timestamp = timestamp(allowNone=False)
    comment = text()
    email = text()
    file = path()

    def tags(self, tag):
        author = tags.span(self.author, class_="author")
        timestamp = self.timestamp.asDatetime().strftime("%m/%d/%y(%a)%H:%M")
        number = "No. %d" % self.number
        return tag(author, timestamp, number, self.comment)
