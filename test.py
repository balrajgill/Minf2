from this import d
import binascii

hex_val = binascii.hexlify(b"test message")

a = int.from_bytes(hex_val,"big")

b = hex(a)

print(hex_val)
print(a)
print(b)
