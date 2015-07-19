#/bin/python

from scapy.all import *
conf.iface = "mon0"


def handle_pkt(pkt):
  if Dot11 in pkt and pkt[Dot11].type == 0 and pkt[Dot11].subtype == 4:
    hwaddr = pkt[Dot11].addr2
    ssid = pkt[Dot11Elt][0].info
    print hwaddr, repr(ssid)

sniff(prn=handle_pkt)
