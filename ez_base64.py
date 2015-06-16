#/bin/python
# Simple b64 wrapper

import base64, sys


class EZ_b64():

	def encode(self, data):
		encoded = base64.b64encode(data)
		print encoded

	def decode(self, data):
		decoded = base64.b64decode(data)
		print decoded


if __name__ == '__main__':
	try:
		opperation = sys.argv[1]
		data = sys.argv[2]
		b64 = EZ_b64()
		if opperation == "encode":	
			b64.encode(data)
		else:
			if opperation == "decode":
				b64.decode(data)
			else:
				print('Usage: ez_b64.py (encode or decode) data')
				sys.exit(1)
	except IndexError:
		print('Usage: ez_b64.py (encode or decode) data')
		sys.exit(1)
