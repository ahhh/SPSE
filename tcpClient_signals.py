#/bin/python
# Program for messing with tcp clients

import socket
import sys
import signal

TARGET_SERVER = ("127.0.0.1", 8888)
tcpSocket = 0

def signal_handler(signum, frm) :
  global tcpSocket
  print "SIGINT received"
  print "Shutting down client gracefully."
  # now shut it down
  tcpSocket.close()
  print "Exiting now."
  sys.exit()

def tcp_client():
  global tcpSocket
  
  tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  tcpSocket.connect(TARGET_SERVER)
  
  signal.signal(signal.SIGINT, signal_handler)

  while 1:
    userInput = raw_input("Please enter a string: ")
    tcpSocket.send(userInput)
    print tcpSocket.recv(1024)
 

if __name__ == '__main__':
  print "Starting tcp client..."
  tcp_client()

  # SIGINT is the signal for program interupt
  signal.signal(signal.SIGINT, signal_handler)
 
  # and now we wait
  while True:
    pass
