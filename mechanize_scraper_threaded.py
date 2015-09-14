#/bin/python
# Program for getting stats out of the Alexa_10000_domains.txt (top alexa domains)
# Example: python mechanize_scraper.py -t Alexa_10000_domains.txt -s robots_directory -p robots.txt -n 10
import mechanize 
import logging
import time
from optparse import OptionParser
from urllib2 import HTTPError
import Queue
import threading
import os

start = time.time()
host_queue = Queue.Queue()

class ScraperThread(threading.Thread):
  def __init__(self, host_queue, page, save):
    threading.Thread.__init__(self)
    self.host_queue = host_queue
    self.page = page
    self.save = save
  
  def run(self):
    while True:
      # Get target host
      target = self.host_queue.get()
      try:
        # Build URL
        url = "http://{0}/{1}".format(target, self.page)
        # Launch browser scraper
        br = mechanize.Browser()
        br.set_handle_equiv(False)
        br.set_handle_redirect(True)
        br.set_handle_referer(False)
        br.set_handle_robots(False)
        scraped = br.open(url)
        saved_name = str(target)+"."+str(self.page)
        with open(os.path.join(self.save, saved_name), 'wb') as temp_file:
          temp_file.write(str(scraped.read()))
        print "Successfully scraped {}".format(url)
      except:
        print "Error with {}".format(target)
      # Complete task in queue
      self.host_queue.task_done()
	  
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

  # Option for targets list to scrape
  optp.add_option("-t", "--targets", dest="targets",
                  help="The list of sites to scan")
				  
  # Option for page to scrape
  optp.add_option("-p", "--page", dest="page",
                  help="The page you want to scrape")
				  
  # Option for saving scraped pages
  optp.add_option("-s", "--save", dest="save",
                  help="The directory you want to save the scraped pages to")
				  
  # Option for number of threads to spawn
  optp.add_option("-n", "--threads", dest="threads",
                  help="The number of threads you want to spawn to do the job")
				  
  opts, args = optp.parse_args()

  if opts.targets is None:
    opts.targets = raw_input("The list of targets to scrape: ")

  if opts.save is None:
    opts.save = raw_input("The directory to save these in: ")
	
  if opts.page is None:
    opts.page = 'index.html'
	
  if opts.threads is None:
    opts.threads = '1'
	
  # Setup logging.
  logging.basicConfig(level=opts.loglevel,
                      format='%(levelname)-8s %(message)s')


  # Main Event Loop:
  try:
  
    # Read and populate the targets thread
    target_list = open(opts.targets)
    for target in target_list.readlines():
      domain = target.split(',')
      domain = domain[1].rstrip()
      host_queue.put(domain)
	  
	# Check to see if the save directory exists, if not create it
    if not os.path.exists(opts.save):
      os.makedirs(opts.save)
	  
    # Spawn # of threads based on user thread option
    for x in range(int(opts.threads)):
      thread = ScraperThread(host_queue, opts.page, opts.save)
      thread.setDaemon(True)
      thread.start()
  
    # Wait for threads to finish
    host_queue.join()
  
  except (KeyboardInterrupt, EOFError) as e:
    print "Exiting..."
    exit(0)

  print "Done! Elapsed Time: {}".format(time.time() - start)

  
if __name__ == '__main__':
  main()
