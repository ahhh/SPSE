#/bin/python

import SocketServer
import SimpleHTTPServer

PORT = 8888

class HTTPRequestHandler (SimpleHTTPServer.SimpleHTTPRequestHandler):

  def do_GET(self):
    if self.path == '/test' :
      self.wfile.write('You have found the test page!')
      self.wfile.write(self.headers)
    else:
      SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


if __name__ == '__main__':
  print "Starting server on port %d"%PORT
  httpServer = SocketServer.TCPServer(("",PORT), HTTPRequestHandler)
  httpServer.serve_forever()
