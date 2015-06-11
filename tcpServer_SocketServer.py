#/bin/python

import SocketServer
import socket

SERVER_ADDRESS = ("0.0.0.0", 8888)

class EchoHandler(SocketServer.BaseRequestHandler):

  def handle(self):
  
    print "Received a connection from: ", self.client_address
    data = "start"
    while len(data):
      data = self.request.recv(1024)
      self.request.send(data)
      print "%s said: "%str(self.client_address), data
	  
    print "%s disconnected"%str(self.client_address)
	

if __name__ == '__main__':

  print "Listening on %s"%str(SERVER_ADDRESS)
  server = SocketServer.TCPServer(SERVER_ADDRESS, EchoHandler)
  server.serve_forever()
