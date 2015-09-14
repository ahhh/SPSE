#!/usr/bin/python
# Inspired by: http://voorloopnul.com/blog/a-python-netstat-in-less-than-100-lines-of-code/

import pwd
import os
import re
import glob

PROC_TCP = "/proc/net/tcp"
STATE = {
        '01':'ESTABLISHED',
        '02':'SYN_SENT',
        '03':'SYN_RECV',
        '04':'FIN_WAIT1',
        '05':'FIN_WAIT2',
        '06':'TIME_WAIT',
        '07':'CLOSE',
        '08':'CLOSE_WAIT',
        '09':'LAST_ACK',
        '0A':'LISTEN',
        '0B':'CLOSING'
        }

def _load():
  # Read the table of tcp connections & remove header  '''
  with open(PROC_TCP,'r') as f:
    content = f.readlines()
    content.pop(0)
  return content

def _hex2dec(s):
  return str(int(s,16))

def _ip(s):
  ip = [(_hex2dec(s[6:8])),(_hex2dec(s[4:6])),(_hex2dec(s[2:4])),(_hex2dec(s[0:2]))]
  return '.'.join(ip)

def _remove_empty(array):
  return [x for x in array if x !='']

def _convert_ip_port(array):
  host,port = array.split(':')
  return _ip(host),_hex2dec(port)

def netstat():
  # Return a list with status of tcp connections at linux systems
  # Run as root to get pid of all network process running on system
  content=_load()
  result = []
  for line in content:
    line_array = _remove_empty(line.split(' '))     # Split lines and remove empty spaces
    l_host,l_port = _convert_ip_port(line_array[1]) # Convert ipaddress and port from hex to decimal
    r_host,r_port = _convert_ip_port(line_array[2]) 
    tcp_id = line_array[0]
    state = STATE[line_array[3]]
    uid = pwd.getpwuid(int(line_array[7]))[0]       # Get user from UID
    inode = line_array[9]                           # Need the inode to get process pid
    pid = _get_pid_of_inode(inode)                  # Get pid from inode
    try:                                            # try read the process name
      exe = os.readlink('/proc/'+pid+'/exe')
    except:
      exe = None

    nline = [tcp_id, uid, l_host+':'+l_port, r_host+':'+r_port, state, pid, exe]
    result.append(nline)
  return result

def _get_pid_of_inode(inode):
  # Check every running process and look for the one using the given inode, to find pid
  for item in glob.glob('/proc/[0-9]*/fd/[0-9]*'):
    try:
      if re.search(inode,os.readlink(item)):
        return item.split('/')[2]
    except:
      pass
  return None

if __name__ == '__main__':
  for conn in netstat():
    print conn
