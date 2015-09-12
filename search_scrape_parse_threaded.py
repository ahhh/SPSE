#!/bin/python
# Inspired by: http://www.ibm.com/developerworks/aix/library/au-threadingpython/
# searches using DuckDuckGo

import Queue
import threading
import urllib2
import time
import re
from BeautifulSoup import BeautifulSoup
		
queries = ["Bakunawa", "Shen-Lung", "Fafnir"]

search_queue = Queue.Queue()
url_queue = Queue.Queue()
out_queue = Queue.Queue()
start = time.time()

class SearcherThread(threading.Thread):
  def __init__(self, search_queue, url_queue):
    threading.Thread.__init__(self)
    self.search_queue = search_queue
    self.url_queue = url_queue
	
  def run(self):
    while True:
      query = self.search_queue.get()
      url = 'http://duckduckgo.com/html/?q='+query
      site = urllib2.urlopen(url)
      data = site.read()
      parsed = BeautifulSoup(data)
      for link in parsed.findAll('div', {'class': re.compile('url')}):
        self.url_queue.put(link.text)
		
      # signals to search_queue job is done
      self.search_queue.task_done()
  

class ScraperThread(threading.Thread):
  def __init__(self, url_queue, out_queue):
    threading.Thread.__init__(self)
    self.url_queue = url_queue
    self.out_queue = out_queue

  def run(self):
    while True:
      # grabs host from queue and crafts url
      host = self.url_queue.get()
      url = "http://"+str(host)
	  
      # grabs urls of hosts and then grabs chunk of webpage
      try:
        url = urllib2.urlopen(url)
        chunk = url.read()
        # place chunk into out queue
        self.out_queue.put(chunk)
      except:
        print '** %s failed to resolve' % (url)
      
      # signals to queue job is done
      self.url_queue.task_done()

	  
class ParserThread(threading.Thread):
  def __init__(self, out_queue):
    threading.Thread.__init__(self)
    self.out_queue = out_queue

  def run(self):
    while True:
      # grabs host from queue
      chunk = self.out_queue.get()
      
      try:
        # parse the chunk
        soup = BeautifulSoup(chunk)
        # Heres where you can scrape any data you want
        print soup.find(['title']).text
        #print soup.find(['body'])
        #print soup.findAll('div', {'class': re.compile('content')})
      except:
        print '** parsing error'

      # signals to queue job is done
      self.out_queue.task_done()


def main():

  for query in queries:
    search_queue.put(query)

  #spawn a pool of DuckDuckGo query threads
  for i in range(3):
    g = SearcherThread(search_queue, url_queue)
    g.setDaemon(True)
    g.start()

  # spawn a pool of threads, and pass them queue instance
  for i in range(10):
    t = ScraperThread(url_queue, out_queue)
    t.setDaemon(True)
    t.start()

  for i in range(10):
    dt = ParserThread(out_queue)
    dt.setDaemon(True)
    dt.start()

  # wait on the queue until everything has been processed
  search_queue.join()
  url_queue.join()
  out_queue.join()
  print "Elapsed Time: %s" % (time.time() - start)
  

if __name__ == '__main__':
  main()
