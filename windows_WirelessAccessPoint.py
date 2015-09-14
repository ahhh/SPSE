# Python wrapper for starting wireless access points on Windows
import time
import logging
import os, sys
from optparse import OptionParser


class AP():
  def __init__(self, opts):
	self.SSID = opts.SSID
	self.KEY = opts.KEY

  def start_AP(self):
    os.popen("netsh wlan set hostednetwork mode=allow ssid={0} key={1}".format(self.SSID, self.KEY))
    os.popen("netsh wlan start hostednetwork")
	
  def stop_AP(self):
    os.popen("netsh wlan stop hostednetwork")
	

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

  # Option for ssid of access point to broadcast
  optp.add_option("-s", "--ssid", dest="SSID",
                  help="The SSID of access point")
  # Option for key to access point
  optp.add_option("-k", "--key", dest="KEY",
                  help="The key for the access point")
				  
  opts, args = optp.parse_args()

  if opts.SSID is None:
    opts.SSID = raw_input("SSID for the access point being broadcast: ")
  if opts.KEY is None:
    opts.KEY = raw_input("Key for the access point being broadcast (8-63 charcters): ")
  
  # Setup logging.
  logging.basicConfig(level=opts.loglevel,
                      format='%(levelname)-8s %(message)s')


  # Main Event Execution:
  try:
    ap = AP(opts)
    ap.start_AP()
    while True:
	  time.sleep(1)
	
  except (KeyboardInterrupt, EOFError) as e:
    ap.stop_AP()
    print "All done!"
    exit(0)
	
  
if __name__ == '__main__':
  main()
