import sys
from twisted.web import server, resource
from twisted.internet import reactor, endpoints


class Counter(resource.Resource):
    isLeaf = True
    numberRequests = 0

    def __init__(self, *args, **kwargs):
        print "Instancai de %s" % self
        resource.Resource.__init__(self, *args, **kwargs)

    def render(self, request):
        print "Estamos accediendo al recurso", request.path
        self.numberRequests += 1
        request.setHeader("content-type", "text/plain")
        return "I am request #" + str(self.numberRequests) + "\n"


try:
    port = int(sys.argv[1])
except:
    port = 8080

endpoints.serverFromString(reactor, "tcp:%s" % port).listen(server.Site(Counter()))
reactor.run()
