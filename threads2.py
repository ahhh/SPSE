#/bin/python
# Program for messing w/ threads and options

import threading
import Queue
import time
import logging
from optparse import OptionParser

continue_threads = True

class WorkerThread(threading.Thread):

  def __init__(self, queue):
    threading.Thread.__init__(self)
    self.queue = queue
	
  def finish(self):
    self.cont = False
	
	
  def run(self):
    print "In WorkerThread"
    while continue_threads == True:
      counter = self.queue.get()
	  # thread Logic goes here
      print "Ordered to sleep for %d seconds!"%counter
      time.sleep(counter)
      print "Finished sleeping for %d seconds"%counter
 
      self.queue.task_done()
  


def main():

  # Setup the command line arguments.
  optp = OptionParser()

  # Output verbosity options
  optp.add_option('-q', '--quiet', help='set logging to ERROR',
                  action='store_const', dest='loglevel',
                  const=logging.ERROR, default=logging.INFO)
  optp.add_option('-d', '--debug', help='set logging to DEBUG',
                  action='store_const', dest='loglevel',
                  const=logging.DEBUG, default=logging.INFO)
  optp.add_option('-v', '--verbose', help='set logging to COMM',
                  action='store_const', dest='loglevel',
                  const=5, default=logging.INFO)

  # Option for number of threads
  optp.add_option("-t", "--threads", dest="threads",
                  help="The number of threads to spawn")
				  
  opts, args = optp.parse_args()

  if opts.threads is None:
    opts.threads = raw_input("How threads do you want to spawn: ")
  
  # Setup logging.
  logging.basicConfig(level=opts.loglevel,
                      format='%(levelname)-8s %(message)s')


  # Main Event Loop:
  try:
    queue = Queue.Queue()
  
    for i in range(int(opts.threads)):
      print "Creating WorkerThread : %d"%i
      worker = WorkerThread(queue)
      worker.setDaemon(True)
      worker.start()
      print "WorkerThread %d Created!"%i

    for j in range(int(opts.threads)):
      queue.put(j)
  
    queue.join()
  
  except (KeyboardInterrupt, EOFError) as e:
    continue_threads = False
    exit(0)
	
  print "All tasks complete!"
  
if __name__ == '__main__':
  main()
