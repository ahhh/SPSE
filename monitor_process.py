# Program for playing with process monitoring
# easy_install psutil
import psutil

monitor_pid = raw_input("What is the pid of the process you wish to monitor: ")
if (psutil.pid_exists(int(monitor_pid))):
  proc = psutil.Process(int(monitor_pid))
  print "Process: {}".format(proc.name())
  print "Located: {}".format(proc.exe())
  print "Created: {}".format(proc.create_time())
  print "By: {}".format(proc.username())
  print "Currently open files: {}".format(proc.open_files())
  print "Current network connections: {}".format(proc.connections())
else: print "The process {} isn't running!".format(monitor_pid)

