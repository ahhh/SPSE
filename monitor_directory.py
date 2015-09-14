#Inspired by example at: https://github.com/gorakhargosh/watchdog#example-api-usage
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

def main():
  logging.basicConfig(level=logging.INFO,
                      format='%(asctime)s - %(message)s',
                      datefmt='%Y-%m-%d %H:%M:%S')
  path = raw_input("What is the path of the directory (and all files recursively) you wish to monitor: ")
  event_handler = LoggingEventHandler()
  observer = Observer()
  observer.schedule(event_handler, path, recursive=True)
  observer.start()
  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    observer.stop()
  observer.join()

if __name__ == "__main__":
  main()
