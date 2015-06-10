#/bin/python
# Program for messing w/ threaded scanning

import threading
import Queue
import time
from scapy.all import *

SOURCE_IP = "127.0.0.1"
TARGET_IP = "127.0.0.1"

class WorkerThread(threading.Thread):

  def __init__(self, queue, tid):
    threading.Thread.__init__(self)
    self.queue = queue
    self.tid = tid
    print "Worker %d Reporting for Duty!" %self.tid
	

  def run(self):
    total_ports = 0
    while True:
      port = 0
      try:
        port = self.queue.get(timeout=1)
      except Queue.Empty:
        print "Worker %d exiting. Scanned %d ports .." %(self.tid, total_ports)
        return
      ip = TARGET_IP
      response = sr1(IP(src=SOURCE_IP, dst=ip)/TCP(dport=port, flags="S"), verbose=False, timeout=.2)
      if response:
        if response[TCP].flags == 18:
          print "ThreadId %d: Received SYN/ACK reply on port %d" %(self.tid, port)

      self.queue.task_done()
      total_ports += 1


if __name__ == '__main__':
  queue = Queue.Queue()
  threads = []
  for i in range(1,10):
    print "Creating WorkerThread : %d"%i
    worker = WorkerThread(queue, i)
    worker.setDaemon(True)
    worker.start()
    threads.append(worker)
    print "WorkerThread %d Created!"%i

  for j in range(1,10):
    queue.put(j)
	
  queue.join()
  
  for item in threads:
    item.join()
  
  print "All tasks complete!"
