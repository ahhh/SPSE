#/bin/python
# Program for messing w/ threaded scanning

import threading
import Queue
import time
from scapy.all import *


class WorkerThread(threading.Thread):

  def __init__(self, queue, tid, target, source):
    threading.Thread.__init__(self)
    self.queue = queue
    self.tid = tid
    self.target = target
    self.source = source
	

  def run(self):
    total_ports = 0
    while True:
      port = 0
      try:
        port = self.queue.get(timeout=1)
      except Queue.Empty:
        print "Worker %d exiting. Scanned %d ports .." %(self.tid, total_ports)
        return
      ip = self.target
      response = sr1(IP(src=self.source, dst=ip)/TCP(dport=port, flags="FPU"), verbose=False, timeout=.5)  #Our XMASScan uses flags Fin, Push, Urgent
      print "Scanning {0}:{1}".format(ip, port)
      if response:
        if (str(type(response)) == "<type 'NoneType'>"): # If response is blank then our port is open
          print "Port: {0} is {1}".format(port, "Open")
        elif response[TCP].flags == 1:			 # If we get a FIN response then our port is closed
          print "Port: {0} is {1}".format(port, "Closed")
        elif ((int(response[ICMP].type) == 3) and (int(response[ICMP].code) in [1,2,3,9,10,13])):  # Certain ICMP responses also indicate the port is filtered
          print "Port: {0} is {1}".format(port, "Filtered") 
      self.queue.task_done()
      total_ports += 1


if __name__ == '__main__':
  queue = Queue.Queue()
  
  source = raw_input("Your IP address or the server you would like to spoof: ")
  target = raw_input("The IP address of the server you wish to scan: ")
  port_range = raw_input("The port range you wish to scan (1-2000): ")
  threads = raw_input("The number of threads would you like to scan with: ")
  port_range = port_range.split('-')
  
  for i in range(int(threads)):
    worker = WorkerThread(queue, i, target, source)
    worker.setDaemon(True)
    worker.start()
    print "WorkerThread %d Created!"%i

  # Scan every port in the range provided
  for j in range(int(port_range[0]),int(port_range[1])):
    queue.put(j)
	
  # Wait for all ports to be scanned
  queue.join()
  print "All tasks complete!"
