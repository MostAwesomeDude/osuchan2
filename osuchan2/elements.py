from twisted.web.template import Element, XMLString, renderer, tags

from osuchan2.items import Post, Thread

class FullBoardElement(Element):

    loader = XMLString("""
        <section
            xmlns:t="http://twistedmatrix.com/ns/twisted.web.template/0.1"
            t:render="threads" />
    """)

    def __init__(self, board):
        self.board = board

    @renderer
    def threads(self, request, tag):
        store = self.board.store
        threads = store.query(Thread, Thread.board == self.board)
        return tag(*[ThreadElement(thread) for thread in threads])

class ThreadElement(Element):

    loader = XMLString("""
        <article
            xmlns:t="http://twistedmatrix.com/ns/twisted.web.template/0.1"
            t:render="header" />
    """)

    def __init__(self, thread):
        self.thread = thread

    @renderer
    def header(self, request, tag):
        subject = "%s - %s [" % (self.thread.author, self.thread.subject)
        link = tags.a("Reply", href="#")
        return tag(subject, link, "]")

class FullThreadElement(Element):

    loader = XMLString("""
        <section
            xmlns:t="http://twistedmatrix.com/ns/twisted.web.template/0.1"
            t:render="posts"
            id="threads">
        </section>
    """)

    def __init__(self, thread):
        self.thread = thread

    @renderer
    def posts(self, request, tag):
        store = self.thread.store
        posts = store.query(Post, Post.thread == self.thread)
        return tag(*posts)

class PostElement(Element):

    loader = XMLString("""
        <article
            xmlns:t="http://twistedmatrix.com/ns/twisted.web.template/0.1">
            <header t:render="header" />
            <section t:render="comment" />
        </article>
    """)

    def __init__(self, post):
        self.post = post

    @renderer
    def header(self, request, tag):
        time = tags.time(str(self.post.timestamp))
        number = "No. %d" % self.post.number
        return tag(self.post.author, time, number)

    @renderer
    def comment(self, request, tag):
        if self.post.file:
            image = tags.img(src=self.post.file)
            return tag(image, self.post.comment)
        else:
            return tag(self.post.comment)
