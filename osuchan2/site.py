from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site

import sys
from twisted.python import log
log.startLogging(sys.stdout)

class OCResource(Resource):
    pass

class OCSite(Site):
    pass

reactor.listenTCP(8080, OCSite(OCResource()))
reactor.run()
