#!/usr/bin/env python
# A dirbuster clone in python
# https://github.com/ahhh/SPSE
import urllib2
import sys
import os

url = sys.argv[1]
open_dir_list = open("dirlist.txt", 'r')
dirs = open_dir_list.read().split("\n")
open_dir_list.close()

for dir in dirs:
    uri = url+"/"+dir
    try:
        response = urllib2.urlopen(uri)
        if response:
            print response.info()
            if response.getcode() == 200:
                print "[+] FOUND %s " % (uri)
    except urllib2.HTTPError, e:
        if e.code == 401:
            print "[!] Authorization Required %s " % (uri)
        elif e.code == 403:
            print "[!] Forbidden %s " % (uri)
        elif e.code == 404:
            print "[-] Not Found %s " % (uri)
        elif e.code == 503:
            print "[!] Service Unavailable %s " % (uri)
        else:
            print "[?] Unknown"
print "\n.:. FINISH .:.\n"
