#/bin/python
# A program for scraping pages and reading the web forms
import mechanize 
import logging
import time
from optparse import OptionParser
from urllib2 import HTTPError

start = time.time()

def get_forms(target):
  br = mechanize.Browser()
  br.set_handle_equiv(False)
  br.set_handle_redirect(True)
  br.set_handle_referer(False)
  br.set_handle_robots(False)
  br.open(target)
  forms = [f for f in br.forms()]
  for form in forms:
    print "Form Name: {}".format(form.name)
    print "Form Action: {}".format(form.action)
    print "Form Method: {}".format(form.method)
    for control in form.controls:
      print "Field: {}".format(control)
	  
	  
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
                  help="The target url to examine")
				  
  opts, args = optp.parse_args()

  if opts.target is None:
    opts.target = raw_input("What is the url of the page you want to examine: ")
	
  # Setup logging.
  logging.basicConfig(level=opts.loglevel,
                      format='%(levelname)-8s %(message)s')


  # Main Event Loop:
  try:
    get_forms(opts.target)
  
  except (KeyboardInterrupt, EOFError) as e:
    print "Exiting..."
    exit(0)

  print "Elapsed Time: %s" % (time.time() - start)
  
if __name__ == '__main__':
  main()
