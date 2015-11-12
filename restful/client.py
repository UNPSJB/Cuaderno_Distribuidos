import sys
try:
    import requests
except ImportError:
    print "pip install requests"
    sys.exit()
from fuse import FUSE, FuseOSError, Operations, LoggingMixIn

response = requests.get('http://localhost:8080/server.py',
                        headers={
                            'X-FS-Op': 'READ'
                        })
print response.content

class RESTFS(Operations):

    def _request(self, path, op, *args):
        headers = {
            'X-FS-Op': op,
            'X-FS-Args': json.dumps(args)
        }
        response = requests.get(
            'http://localhost:8080/%s' % path, headers=headers
        )
        return json.loads(response.content)
    def access(self, path, mode):
        self._request(path, 'access', mode)

    def readdir(self, path, fh):
        return self._request(path, 'readdir')

    def read(self, path, size, offset, fh):
        return self._request(path, 'readdir')[offset:offset+size]

    def write(self, path, data, offset, fh):





    def __init__(self, )
if __name__ == '__main__':


    fuse = FUSE(RESTFS(sys.argv[1]), foreground=True)
