# Ahhh requests w/ Malwr API

from optparse import OptionParser
import logging
import requests
from requests.auth import HTTPBasicAuth

# Function to run our upload
def uploadToMalwr(file_upload, apikey):
  url = 'https://malwr.com/api/analysis/add/'
  files = {'file': (file_upload, open(file_upload, 'rb'), 'application/octet-stream', {'Expires': '0'})}
  data = {'api_key': apikey, 'shared': 'yes', 'force': 'True'}
  return requests.post(url, files=files, data=data, verify=True)
  
# Function to run our check
def checkMalwr(uuid, apikey):
  url = 'https://malwr.com/api/analysis/status/'
  data = {'api_key': apikey, 'uuid': uuid}
  return requests.post(url, verify=True)


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

  # Option for file to upload
  optp.add_option("-f", "--file", dest="file_upload",
                  help="The file you want to upload")
				  
  # Option for hash to download
  optp.add_option("-i", "--id", dest="uuid",
                  help="The hash of the file you want to download")
				  
  # Option for URL to upload to
  optp.add_option("-k", "--key", dest="apikey",
                  help="The apikey for the service")

  opts, args = optp.parse_args()				  
  # Prompt if the user disn't give a apikey
  if opts.apikey is None:
    opts.apikey = raw_input("What's your Malwr API key? ")
	
  results = "You need to upload a file (-f) or look up a uuid (-c)"
  
  # Run upload if the user gave us a file to upload
  if opts.file_upload is not None:
    # Run our upload function	
    results = uploadToMalwr(opts.file_upload, opts.apikey)
	
  #  Run Download if the user gave us a hash to get
  if opts.uuid is not None:
    # Run our download function	
    results = checkMalwr(opts.uuid, opts.apikey)
  
  for result in results:
    print result


if __name__ == '__main__':
  main()
