# Ahhh requests w/ freegeoip API

from optparse import OptionParser
import logging
import requests
import json


def queryFreeGeo(query):
  response = requests.get('http://www.freegeoip.net/json/' + query)
  api_response = []
  if response.status_code == 200:
    body = json.loads(response.text)
    for key, value in body.iteritems():
      api_response.append(str(key) + ': ' + str(value))
    return '\n'.join(api_response)
  return "Apologies but freegeoip.net is not responding right now."

	
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

  # Option for URL to upload to
  optp.add_option("-i", "--ip", dest="query",
                  help="The IP address you want to lookup")

  opts, args = optp.parse_args()				  
  
  if opts.query is None:
    opts.query = raw_input("What's your IP query? ")
	
  results = queryFreeGeo(opts.query)

  print results

if __name__ == '__main__':
  main()
