# Ahhh requests w/ Viper API

from optparse import OptionParser
import logging
import requests
from requests.auth import HTTPBasicAuth

# Function to run our upload
def uploadToViper(user, passw, file_upload, endpoint):
  url = 'http://'+endpoint+'/file/add'
  files = {'file': (file_upload, open(file_upload, 'rb'), 'application/octet-stream', {'Expires': '0'})}
  data = {'file_name': file_upload}
  return requests.post(url, auth=HTTPBasicAuth(user, passw), files=files, data=data, verify=False)
  
# Function to run our download
def downloadFromViper(user, passw, hash, endpoint):
  url = 'http://'+endpoint+'/file/get/'+hash
  return requests.get(url, auth=HTTPBasicAuth(user, passw), verify=False)


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

  # Option for user for basic auth
  optp.add_option("-u", "--user", dest="user",
                  help="The user for the basic auth")

  # Option for password for basic auth
  optp.add_option("-p", "--passw", dest="passw",
                  help="The password for the basic auth")
				  
  # Option for file to upload
  optp.add_option("-f", "--file", dest="file_upload",
                  help="The file you want to upload")
				  
  # Option for hash to download
  optp.add_option("-m", "--md5", dest="file_hash",
                  help="The hash of the file you want to download")
				  
  # Option for URL to upload to
  optp.add_option("-e", "--endpoint", dest="api_endpoint",
                  help="The url you want to upload to")


  opts, args = optp.parse_args()
  # Prompt if the user dosn't give creds for basic auth
  if opts.user is None:
    opts.user = raw_input("What user are you giving to log in? ")

  # Prompt if the user dosn't give creds for basic auth
  if opts.passw is None:
    opts.passw = raw_input("What pass are you giving to log in? ")
	
  # Prompt if the user disn't give a url to upload
  if opts.api_endpoint is None:
    opts.api_endpoint = raw_input("What's the host of the Viper API endpoint? ")
    # Example: opts.api_endpoint = 'viperhost:9002'
	
  results = "You need to upload a file (-f) or look up a hash (-m)"
  
  # Run upload if the user gave us a file to upload
  if opts.file_upload is not None:
    # Run our upload function	
    results = uploadToViper(opts.user, opts.passw, opts.file_upload, opts.api_endpoint)
	
  #  Run Download if the user gave us a hash to get
  if opts.file_hash is not None:
    # Run our download function	
    results = downloadFromViper(opts.user, opts.passw, opts.file_hash, opts.api_endpoint)
  
  for result in results:
    print result


if __name__ == '__main__':
  main()
