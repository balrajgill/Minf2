from hmac import digest
from msilib.schema import MsiFileHash
from sys import argv
from hashlib import sha256, sha1
from random import getrandbits
import binascii
from web3 import Web3
from Crypto.Hash import keccak


def getCommitment(msg):
        key = "{0:0{1}x}".format(getrandbits(256), 64)
        #print(key) 
        com = Web3.soliditySha3(['string'], [key+msg])
        
        return ((com.hex()[2:]),key)
    
def verify(msg,commitment,key): 
    
    return commitment == (((Web3.solidityKeccak(['string'], [key+msg])).hex())[2:])

com,key = getCommitment("1")
print(verify("1",com,key))
print(key)
print(com)
print(com.encode())
    
    
    

k = keccak.new(digest_bits = 256)

k.update((key+"1").encode())
print (k.hexdigest())