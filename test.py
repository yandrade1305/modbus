import struct
command = 0xB1
message = 2
identifier = '0601'

little = [
	*list(struct.pack("<i" if isinstance(message, int) else "f", message)),
]

big = [
	*list(struct.pack(">i" if isinstance(message, int) else "f", message)),
]

print(little)
print(bytes(little))
print(int.from_bytes(bytes(little), 'little'))

print(big)
print(bytes(big))
print(int.from_bytes(bytes(big), 'big'))