import sys
import struct # https://docs.python.org/2/library/struct.html#struct.pack
from crc import get_crc16
import constants as C

class Modbus:
	def __init__(self):
		self.__identifier = '0601'
		self.request = [0xA1, 0xA2, 0xA3]
		self.send	= [0xB1, 0xB2, 0xB3]

	def create_package(self, register_addr, func_code, data):
		byte_array = []
		if data[0] in self.request:
			# Request Data
			byte_array = [
				register_addr
				, func_code
				, *data
				, *self.enrollment_id
			]
		else:
			# Send Data
			message, command = self.cast(data[0])
			if isinstance(message, str):
				byte_array = [
					register_addr
					, func_code
					, command
					, len(message)
					, *[ord(char) for char in message]
					# , *self.enrollment_id
				]
			else:
				byte_array = [
					register_addr
					, func_code
					, command
					, *list(struct.pack("i" if isinstance(message, int) else "f", message))
					# , *self.enrollment_id
				]
		crc = get_crc16(byte_array)
		byte_array = byte_array + list(struct.pack('H', crc))
		return byte_array

	def cast(self, value):
		if value.isdigit():
			return int(value), 0xB1
		elif value.replace('.', '', 1).isdigit():
			return float(value), 0xB2
		else:
			return value, 0xB3

	@property
	def enrollment_id(self):
		return [int(num) for num in str(self.__identifier)]