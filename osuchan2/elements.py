from twisted.web.template import Element, XMLString, renderer, tags

class ThreadElement(Element):

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
