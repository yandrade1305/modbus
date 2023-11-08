from modbus import Modbus
from uart import UART
import constants as C
import time
import os
import struct # https://docs.python.org/3/library/struct.html
import signal

class Program:
	def __init__(self):
		self.message = Modbus()
		self.uart = UART()
		signal.signal(signal.SIGINT, self.signal_handler)
	
	def clear(self):
		os.system('clear' if os.name == 'posix' else 'clear')

	def signal_handler(self, signal, frame):
		self.uart.close()
		print("\nForcefully ending program...")
		exit(0)

	def start(self):
		while True:
			self.menu()
			option = input()

			try:
				option = int(option)
			except:
				continue

			if option == 0:
				self.uart.close()
				exit()
			elif option == 1:
				self.send_message()
			elif option == 2:
				self.request_menu()
				option = input()
				while True:
					try:
						option = int(option)
					except:
						option = input()
						continue
					if option == 1:
						value = "INT"
					elif option == 2:
						value = "FLOAT"
					elif option == 3:
						value = "STRING"
					else:
						break
					print(self.get_message(C.request_menu[value]))
					option = input()
	
		self.uart.close()

	def menu(self):
		# self.clear()
		print('------------ MENU -----------')
		print('(0) Exit')
		print('(1) Send data')
		print('(2) Request data')

	def request_menu(self):
		# self.clear()
		print('-------- REQUEST DATA -------')
		print('(0) Go back')
		print('(1) Request INTEGER')
		print('(2) Request FLOAT')
		print('(3) Request STRING')

	def send_message(self):
		msg = input('Type in your message: ')
		self.uart.write(self.message.create_package(register_addr=C.destination_register, func_code=0x16, data=[msg]))
		time.sleep(1)

	def get_message(self, command):
		msg = self.message.create_package(register_addr=C.destination_register, func_code=0x23, data=[command])
		self.uart.write(msg)
		time.sleep(1)
		if command == C.request_menu["STRING"]:
			origin_register, code, subcode, msg_len = struct.unpack("BBBB", self.uart.read(bytes=4))
			msg = self.uart.read(bytes=msg_len)
			crc = self.uart.read(bytes=2)
			return(msg.decode('utf-8'))
		else:
			origin_register, code, subcode, num, crc = struct.unpack(f'<BBB{"i" if command == C.request_menu["INT"] else "f"}H', self.uart.read(bytes=9))
			return(num)