#!/bin/python
# Inspired by: https://bitbucket.org/whyJoseph/spse-whyjoseph/src/a9cb102ae93826cd7155ff77c2c4a24f584ff0a3/SANSTopXIP.py
from optparse import OptionParser
import logging
import urllib
import re
import sys
# Uses BeautifulSoup4
from bs4 import BeautifulSoup


def threatIPs(quantity):
  page = urllib.urlopen("http://isc.sans.edu/sources.html")
  parsed = BeautifulSoup(page.read(), "html.parser")
  counter = 0
  results = []
  for link in parsed.find_all('a'):
    if (re.search('ipinfo', str(link)) and (counter < int(quantity))):
      results.append(link.string)
      counter += 1
  return results

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

  optp.add_option("-n", "--quantity", dest="quantity",
                  help="The quantity of IP addresses to fetch from the threat feed")
				  
  opts, args = optp.parse_args()

  if opts.quantity is None:
    opts.quantity = 100
	
  results = threatIPs(opts.quantity)
  for result in results:
    print result


if __name__ == '__main__':
  main()
