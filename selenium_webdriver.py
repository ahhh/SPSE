#/bin/python
# Program for messing with web driver
from selenium import webdriver
import logging
from optparse import OptionParser
from urlparse import urlparse


def screen_cap(site, output):
  driver = webdriver.Firefox()
  driver.set_window_size(1024,480)
  driver.get(site)
  driver.save_screenshot(output)
  driver.quit()


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

  # Option for site to browse to
  optp.add_option("-s", "--site", dest="site",
                  help="The site to browse to")
				  
  # Option for name of the screenshot
  optp.add_option("-o", "--out", dest="output",
                  help="The name the screenshot saves to")
				  
  opts, args = optp.parse_args()

  if opts.site is None:
    opts.site = raw_input("which site do you want to browse to: ")
	
  if opts.output is None:
    parsed = urlparse(opts.site)
    domain = parsed.netloc
    opts.output = str(domain)+".png"
    print "Output file not specified, saving as: "+opts.output

  # run main functions
  screen_cap(opts.site, opts.output)
  
if __name__ == '__main__':
  main()
