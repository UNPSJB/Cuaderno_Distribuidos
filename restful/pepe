import sys
try:
    import twisted
except ImportError:
    print "pip install requests"
    sys.exit()


from twisted.web import server, resource
from twisted.internet import reactor
import json
import os

class Simple(resource.Resource):
    isLeaf = True
    def render(self, request):

        path, method, op = request.path, request.method, request.getHeader('X-FS-Op')
        method = method.upper()
        if not op:
            return "Falta HEADER X-FS-Op"
        op = op.upper()
        path = path[1:]

        if method == "GET":
            if op == "ACCESS":
                return json.dumps({
                    'result': True
                })
            elif op == "READ":
                with open(path) as fp:
                    return fp.read()
            elif op == "GETATTR":
                st = os.lstat(path)
                valor = dict((key, getattr(st, key)) for key in (
                             'st_atime', 'st_ctime',
                             'st_gid', 'st_mode', 'st_mtime',
                             'st_nlink', 'st_size', 'st_uid'))
                return json.dumps(valor)
            elif op == "READDIR":
                valor = ['.', '..'] + os.listdir(path or '.')
                return json.dumps(valor)

        elif method == "POST":
            print "Vamos a escribr"
            with open(path, 'w') as fp:
                fp.write(request.content.getvalue())
        elif method == "PUT":
            pass
        elif method == "DELETE":
            pass


        return request.path

site = server.Site(Simple())
reactor.listenTCP(8080, site)
reactor.run()
