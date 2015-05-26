#!/usr/bin/env python
# Arp scanner

# Suppress warning messages from Scapy, but show errors.
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *

SUBNET = "192.168.1."
HOST_RANGE_START = 1
HOST_RANGE_END = 254

for host in range(HOST_RANGE_START,HOST_RANGE_END):
  ip = SUBNET +str(host)
  arpRequest = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip, hwdst="ff:ff:ff:ff:ff:ff")
  arpResponse = srp1(arpRequest, timeout=1, verbose=0)
  if arpResponse:
    print "IP: " + arpResponse.psrc + " MAC: " + arpResponse.hwsrc
