#/bin/python
# Program for reading from USB related messages from syslog

import os, sys

def get_usb_messages():
  with open("/var/log/syslog") as f:
    for line in f:
      if "usb" in line.lower():
        print line
		
if __name__ == '__main__':
  get_usb_messages()
