from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET, Site
from twisted.web.template import flatten

import sys
from twisted.python import log
log.startLogging(sys.stdout)

from axiom.store import Store

from osuchan2.elements import IndexElement

store = Store()

class OCIndex(Resource):

    isLeaf = True

    def render_GET(self, request):
        element = IndexElement(store)
        d = flatten(request, element, request.write)
        d.addCallback(lambda none: request.finish())
        return NOT_DONE_YET

root = Resource()
root.putChild("", OCIndex())

site = Site(root)
