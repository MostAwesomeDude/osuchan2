from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.web.template import flatten

import sys
from twisted.python import log
log.startLogging(sys.stdout)

from axiom.store import Store

from osuchan2.elements import FullBoardElement, IndexElement
from osuchan2.items import Board

class OCBoard(Resource):

    isLeaf = True

    def __init__(self, board):
        self.board = board

    def render_GET(self, request):
        element = FullBoardElement(self.board)
        d = flatten(request, element, request.write)
        d.addCallback(lambda none: request.finish())
        return NOT_DONE_YET

class OCIndex(Resource):

    isLeaf = True

    def __init__(self, store):
        self.store = store

    def render_GET(self, request):
        element = IndexElement(self.store)
        d = flatten(request, element, request.write)
        d.addCallback(lambda none: request.finish())
        return NOT_DONE_YET

class OCRoot(Resource):

    def __init__(self, boards=[], *args, **kwargs):
        Resource.__init__(self)

        self.store = Store(*args, **kwargs)

        index = OCIndex(self.store)
        self.putChild("", index)
        self.putChild("index", index)

        for abbreviation, name in boards:
            self.add_board(abbreviation, name)

    def add_board(self, abbreviation, name):
        board = self.store.findOrCreate(Board, abbreviation=abbreviation,
            name=name)
        self.putChild(abbreviation, OCBoard(board))
