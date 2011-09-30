from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site

import sys
from twisted.python import log
log.startLogging(sys.stdout)

from axiom.store import Store

store = Store()

class OCIndex(Resource):

    isLeaf = True

    def render_GET(self, request):
        return "Hi!"

root = Resource()
root.putChild("", OCIndex())

reactor.listenTCP(8080, Site(root))
reactor.run()
