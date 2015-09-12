from BeautifulSoup import BeautifulSoup
from optparse import OptionParser
import logging
import urllib
import re


# Search function takes any string query and returns a list of urls from DuckDuckGo
def searchDDG(query):
  site = urllib.urlopen('http://duckduckgo.com/html/?q={0}'.format(query))
  data = site.read()
  parsed = BeautifulSoup(data)
  results = []
  for url in parsed.findAll('div', {'class': re.compile('url')}):
    results.append(url.text)	
  return results
  
# Main function with options for running script directly
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

  # Option for search query
  optp.add_option("-g", "--query", dest="query",
                  help="The search query to send to DuckDuckGo")
				  
  opts, args = optp.parse_args()
  # Prompt if the user disn't give a search query
  if opts.query is None:
    opts.query = raw_input("What is your search query for DuckDuckGo? ")
	
  results = searchDDG(opts.query)
  for result in results:
    print result


if __name__ == '__main__':
  main()
