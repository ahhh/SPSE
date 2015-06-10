#! /bin/python
# Program for messing with tcp server and signals 

import sys, signal, socket, random

# set our socket as a global variable
s = 0
 
def signal_handler(signum, frm) :
  global s
  print "SIGINT received"
  print "Shutting down listener gracefully."
  # now shut it down
  s.close()
  print "Exiting now."
  sys.exit()

def tcp_listner():
  global s
  # pick a random port and fetch host
  port = random.randrange(18000,65535,1)
  host = socket.gethostname()
 
  # point SIGINT to signal_handler 
  signal.signal(signal.SIGINT, signal_handler)

  print "Opening port %d." % (port)
  try: 
    # try to create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  except socket.error:
    print 'Socket creation failed!'
    sys.exit()
 
  print "Binding to host %s port %d" % (host,port)
  s.bind((host,port))
  # open up a listener that will accept 1 connection
  s.listen(1)

if __name__ == '__main__':
  print "Starting tcp listner..."
  tcp_listner()

  # SIGINT is the signal for program interupt
  signal.signal(signal.SIGINT, signal_handler)
 
  # and now we wait
  while True:
    pass
