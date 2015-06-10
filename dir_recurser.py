#/bin/python
# Program for messing around with files and directories recursivly
import os, sys
from os.path import join, getsize

def dir_recurse(target_directory):
  for root, dirs, files in os.walk(target_directory):
    print "Contents of directory: ", root
    for file in files:
      print str(os.path.getsize(os.path.join(target_directory, file)))+": "+file
    for dir in dirs:
      dir_recurse(os.path.join(target_directory, dir))
    break
  
  
if __name__ == '__main__':
  try:
    target_dir = sys.argv[1]
    dir_recurse(target_dir)
  except IndexError:
    print "python dir_recurser.py [/full/path/of/target/dir]"
