from this import d
import binascii
from weakref import WeakValueDictionary

msg = "528dc343ef11011fb5a736aef44d70f7fc02b2452fce9cd0587a36cd1f8f8d2b"
hex_val = binascii.hexlify(msg.encode())

a = int(hex_val,16)
b = hex(a)[2:]
c = bytes.fromhex(b)
print(msg)
print(int(hex_val))
print(a)
print(b)
print(c.decode())


ganache_url = "http://127.0.0.1:7545"
from web3 import Web3
web3 = Web3(Web3.HTTPProvider(ganache_url))
print(web3.eth.accounts.create())