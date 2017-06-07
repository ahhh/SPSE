 # Ahhh requests w/ ShadowServer API

from optparse import OptionParser
import logging
import requests

# Function to run our check
def checkSS(ioc):
  url = "https://innocuous.shadowserver.org/api/?query=" + ioc
  if "," in ioc:
    url = "https://innocuous.shadowserver.org/api/?query="
    args = ioc.split(",")
    results = []
    for arg in args:
      results.append(requests.get(url + arg).text)
    return "Shadow Server Results: " + "\n\n".join(results)

  results = requests.get(url)
  return "Shadow Server Results: " + results.text
		

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

  # Option for hash to download
  optp.add_option("-i", "--ioc", dest="ioc",
                  help="The hash, ip, or domain of the ioc you want to check")

  opts, args = optp.parse_args()			
  
  # Prompt if the user disn't give an ioc
  if opts.ioc is None:
    opts.ioc = raw_input("What's your IOC (Hash, ip, domain)? ")
	
  results = checkSS(opts.ioc)

  print results


if __name__ == '__main__':
  main()
