from socket import *
import time
from optparse import OptionParser
import logging


class monitor_TCP():
  def __init__(self, opts):
    self.rawSocket = socket(AF_INET, SOCK_RAW, IPPROTO_TCP)
    self.rawSocket.bind((opts.listen, 0))

  def listen_SYN(self):
    # Function holds till it receives a packet
    data = self.rawSocket.recv(2048)

    # http://en.wikipedia.org/wiki/IPv4#Packet_structure
    # Internet Header Length; Have to determine where the IP header ends
    ihl = ord(data[0]) & 15
    ip_payload = data[ihl*4:]

    # http://en.wikipedia.org/wiki/Transmission_Control_Protocol#TCP_segment_structure
    # Match SYN but not SYN/ACK
    if (ord(ip_payload[13]) & 18) == 2:
      src_addr = inet_ntoa(data[12:16])
      dst_addr = inet_ntoa(data[16:20])
      # Could use struct.unpack, might be clearer
      src_port = (ord(ip_payload[0]) << 8) + ord(ip_payload[1])
      dst_port = (ord(ip_payload[2]) << 8) + ord(ip_payload[3])
      src_str = (src_addr+':'+str(src_port)).ljust(22)
      dst_str = (dst_addr+':'+str(dst_port))
      return "%s=> %s" % (src_str, dst_str)
	  
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
  optp.add_option("-l", "--listen", dest="listen",
                  help="The IP address of the interface to listen on (default is 0.0.0.0, aka all)")
  # Option for key to access point
  optp.add_option("-n", "--number", dest="number",
                  help="The number of packets to capture (default is 0, aka infinite)")
  optp.add_option("-t", "--timeout", dest="timeout",
                  help="The number of minutes to listen before it times out (default is 0, aka infinite)")
				  
  opts, args = optp.parse_args()

  if opts.listen is None:
    opts.listen = "0.0.0.0"
  if opts.number is None:
    opts.number = "0"
  if opts.timeout is None:
    opts.timeout = "0"
  
  # Setup logging.
  logging.basicConfig(level=opts.loglevel,
                      format='%(levelname)-8s %(message)s')


  # Main Event Execution:
  try:
    timeout = time.time() + 60*int(opts.timeout)   # 5 minutes from now
    max_number = 0  # max number of packets to capture counter
    monitor = monitor_TCP(opts)
    while True:
      print monitor.listen_SYN()
      max_number = max_number + 1
      if (max_number == int(opts.number)) or ((int(opts.timeout) != 0) and (time.time() > timeout)):
        break
	
  except (KeyboardInterrupt, EOFError) as e:
    print "All done!"
    exit(0)
	
  
if __name__ == '__main__':
  main()
