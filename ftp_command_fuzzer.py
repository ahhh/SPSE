#/bin/python
# Program for fuzzing arbitrary tcp servers //with connector applied to an ftp server

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
  
def ftp_login():
  global tcpSocket
  signal.signal(signal.SIGINT, signal_handler)
  tcpSocket.send('USER '+ftp_login_user+'\r\n')
  tcpSocket.recv(1024)
  tcpSocket.send('PASS '+ftp_login_pass+'\r\n')
  tcpSocket.recv(1024)
  
def fuzz_client(commands, hot_fuzz):
  global tcpSocket
  signal.signal(signal.SIGINT, signal_handler)
  for command in commands:
    print "Running through fuzzing loop using command: "+command
	for fuzz in hot_fuzz:
      tcpSocket.send(command+' '+fuzz+'\r\n')
      print tcpSocket.recv(1024)
 

if __name__ == '__main__':
  print "Starting fuzzing client..."
  command_file = raw_input("Please enter the location of the command string file: ")
  try:
    commands = open(command_file, 'rb').read()
  except:
    print "could not open command file!"  
    exit
	
  fuzz_file = raw_input("Please enter the location of the fuzz string file: ")
  try:
    hot_fuzz = open(fuzz_file, 'rb').read()
  except:
    print "could not open fuzz file!"  
    exit
  
  tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  tcpSocket.connect(TARGET_SERVER)
  
  ftp_login()
  fuzz_client(commands, hot_fuzz)

  # SIGINT is the signal for program interrupt
  signal.signal(signal.SIGINT, signal_handler)
 
  # and now we wait
  while True:
    pass
