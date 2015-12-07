#/bin/python
# Program for fuzzing / attacking an ftp PASS field

import socket
import sys
import signal

TARGET_SERVER = ("127.0.0.1", 8888)
ftp_login_user = 'test'
ftp_login_pass = 'test'
tcpSocket = 0

def signal_handler(signum, frm) :
  global tcpSocket
  print "SIGINT received"
  print "Shutting down client gracefully."
  # now shut it down
  tcpSocket.close()
  print "Exiting now."
  sys.exit()
  
def fuzz_client(hot_fuzz):
  global tcpSocket
  
  tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  tcpSocket.connect(TARGET_SERVER)
  
  signal.signal(signal.SIGINT, signal_handler)
  
  for fuzz in hot_fuzz:
    tcpSocket.send('USER '+ftp_login_user+'\r\n')
    print tcpSocket.recv(1024)	
    tcpSocket.send('PASS '+fuzz+'\r\n')
    print 'Pass '+fuzz
    print tcpSocket.recv(1024)	
 

if __name__ == '__main__':
  print "Starting fuzzing client..."
  fuzz_file = raw_input("Please enter the location of the fuzz string file: ")
  try:
    hott_fuzz = open(fuzz_file, 'rb').read()
	hot_fuzz = hott_fuzz.split()
  except:
    print "could not open fuzz file!"  
	exit
 
  fuzz_client(hot_fuzz)

  # SIGINT is the signal for program interrupt
  signal.signal(signal.SIGINT, signal_handler)
 
  # and now we wait
  while True:
    pass
