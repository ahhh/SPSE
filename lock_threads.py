#/bin/python
# Program to mess with locking threads in python

 
import thread
import threading
import time
 
counter = 0
lock = threading.Lock()
active = 0
 
def process_item():
  global counter, lock
  lock.acquire()
  counter += 1
  lock.release()
 
def worker_thread(id) :
  global active
  print "Thread id %d now alive!"%id
  for i in range(100000):
    process_item()
  active -= 1
  print "Thread id %d now done."%id

  
if __name__ == '__main__':
  for i in range(7):
    active += 1
    thread.start_new_thread(worker_thread, (i,))
 
  while active > 0:
    pass
 
  print "counter = ",counter, " (it should be 700000)."
