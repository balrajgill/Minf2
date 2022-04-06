from msilib.schema import MsiFileHash
from sys import argv
from hashlib import sha256
from random import getrandbits
import binascii
from web3 import Web3
def getCommitment(msg):
        key = "{0:0{1}x}".format(getrandbits(256), 64) 
        com = Web3.solidityKeccak(['string'], [key+msg])
        
        return (com.hex(),key)
    
def verify(msg,commitment,key):   
    return commitment == (Web3.solidityKeccak(['string'], [key+msg])).hex()




if __name__ == '__main__':
    commit,key = getCommitment("testing")
    key = "7ca51aedc46cfa0470b187d0f8cf0e0eb2450b8672096b30d4d5418bed18ffe7"
    commit = "0x0aac5107c75ca15e39819b6011a326c3dbb48689a61bf5f95457292e47f0834c"
    print(verify("testing",commit,key))
    print(commit)
    
    
    
