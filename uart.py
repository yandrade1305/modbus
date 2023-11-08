import serial # https://pythonhosted.org/pyserial/pyserial_api.html#classes

class UART:
	def __init__(self):
		self.__port = '/dev/serial0'
		self.__baudrate = 9600
		self.__bytesize = serial.EIGHTBITS

		self.channel = serial.Serial(port=self.__port, baudrate=self.__baudrate, bytesize=self.__bytesize, timeout=1500)
		self.channel.reset_input_buffer()
		self.channel.reset_output_buffer()

	def write(self, package):
		self.channel.write(bytes(package))

	def read(self, bytes):
		byte_array = self.channel.read(size=bytes)
		while len(byte_array) < bytes:
			byte_array = byte_array + [self.channel.read(size=bytes)]
		return byte_array
	
	def close(self):
		if self.channel.is_open:
			self.channel.close()

	def open(self):
		if not self.channel.is_open:
			self.channel.open()
			self.channel.reset_input_buffer()
			self.channel.reset_output_buffer()