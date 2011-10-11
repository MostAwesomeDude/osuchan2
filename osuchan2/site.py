from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET, Site
from twisted.web.template import flatten

import sys
from twisted.python import log
log.startLogging(sys.stdout)

from axiom.store import Store

from osuchan2.elements import FullBoardElement, IndexElement
from osuchan2.items import Board

store = Store()

boards = [u"co", u"d"]

class OCRoot(Resource):

    isLeaf = True

    def render_GET(self, request):
        element = IndexElement(store)
        d = flatten(request, element, request.write)
        d.addCallback(lambda none: request.finish())
        return NOT_DONE_YET

class OCBoard(Resource):

    isLeaf = True

    def __init__(self, board_name):
        self.board = store.findOrCreate(Board, abbreviation=board_name)

    def render_GET(self, request):
        element = FullBoardElement(self.board)
        d = flatten(request, element, request.write)
        d.addCallback(lambda none: request.finish())
        return NOT_DONE_YET

root = Resource()
root.putChild("", OCRoot())

for board in boards:
    root.putChild(board, OCBoard(board))

site = Site(root)
