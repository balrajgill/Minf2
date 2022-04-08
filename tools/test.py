from this import d
import binascii
from weakref import WeakValueDictionary
from web3 import Web3
import random


msg = "testing"
msg2 = "test"
i = int.from_bytes(msg.encode('ascii'), byteorder='little')
print(i)
i2 = int.from_bytes(msg2.encode('ascii'), byteorder='little')
print(i2)
