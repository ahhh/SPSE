#!/usr/bin/env python
# Python script for playing around with FTP servers
 
import ftplib
 
# Connection information
server_list = 'ftps2.txt'
username = 'anonymous'
password = 'anonymous'
 
# Directory and matching information
directory = '/'
filematch = '*'

# Establish the connection
def ftp_connect(server):
  ftp = ftplib.FTP(server)
  ftp.login(username, password)
  print "Logged into "+str(server)
  return ftp
  
# Loop through matching files and download each one individually
def grab_files(ftp, filesmatch):
  for filename in ftp.nlst(filematch):
    fhandle = open(filename, 'wb')
    print 'Getting ' + filename
    ftp.retrbinary('RETR ' + filename, fhandle.write)
    fhandle.close()
	
def list_files(ftp, filesmatch):
  print "Reading from: "+str(ftp.cwd(directory))
  for filename in ftp.nlst():
    print filename
	
def ftp_explore(server):
  ftp = ftplib.FTP(server)
  ftp.login(username, password)
  print "Logged into "+str(server)
  ftp.cwd(directory)
  print "Reading from: "+str(directory)
  for filename in ftp.nlst():
    print filename  
	
if __name__ == '__main__':
  f = open(server_list)
  for line in f.readlines():
    print "Trying to connect to "+str(line)
    try:
      line = line.strip('\n')
      ftp_explore(line)
    except:
      print "Could not connect to "+str(line)	

	
