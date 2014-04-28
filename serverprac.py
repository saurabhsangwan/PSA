import sys
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import finalimagesuggestion as IS
class MyHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        print "POST"
        length = int(self.headers.getheader('content-length'))
        input = self.rfile.read(length)
        n = IS.NLTK()
        resp = n.entities(input)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(resp)
     

HandlerClass = MyHandler
ServerClass  = BaseHTTPServer.HTTPServer
Protocol     = "HTTP/1.0"

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000
server_address = ('127.0.0.1', port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)

sa = httpd.socket.getsockname()
print "Serving HTTP on", sa[0], "port", sa[1], "..."
httpd.serve_forever()
