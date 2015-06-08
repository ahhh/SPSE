#/bin/python
# Python program for playing around with user defined exceptions

class TooSmallError(Exception):
  message = "Too small! Try again ;)"

class TooBigError(Exception):
  message = "Too big! Try again ;)"
 
class ExactError(Exception):
  def __init__(self):
    print "HAHAHA You hit the trap"
	 
class unhandledError(Exception):pass

def checkNumber(num):
  if(num <= 4):
    raise TooSmallError
  elif(num >= 7):
    raise TooBigError
  elif(num == 5):
    raise ExactError
  return num
  
while 1:
  try:
    usrInpt = int(raw_input("Enter the magic number: "))
    print checkNumber(usrInpt)
  except TooSmallError, e:
    print e.message
  except TooBigError, e:
    print e.message
  except ExactError, e:
    print e.message
  else:
    break
  
