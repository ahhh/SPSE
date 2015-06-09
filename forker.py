#/usr/bin/python
# Python program for playing around with forking
import os, sys

def child_process():
  print "I am a child process and my PID is : %d"%os.getpid()
  
  
def forking_process(children):
    children = int(children) - 1
    childpid = os.fork()

    if childpid == 0 :
      # this is the child process
      child_process()
    else:
      print "I am a parent process with PID : %d"%os.getpid()
      print "Spawned child with PID : %d"%childpid
	  if children != 0:
	    forking_process(children)


if __name__ == '__main__':
  try:  
    children = sys.argv[1]
    forking_process(children)

  #exception handling
  except IndexError:
    print "python forker.py [#_of_children]"
