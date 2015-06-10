#/bin/python
# Program for messing around with signal handlers

import signal

def ctrl_c_handler(signum, frm):
  print "Lol! Can't kill me, I'm the program gingerbread man!!"
  
if __name__ == '__main__':
  print "Setting up signal handlers..."
  
  # SIGINT is the signal for program interupt
  signal.signal(signal.SIGINT, ctrl_c_handler)
  
  print "Done!"
  
  while True:
    pass
