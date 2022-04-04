from sys import argv
from hashlib import sha256
from random import getrandbits
import binascii

def getCommitment(msg):
        key = "{0:0{1}x}".format(getrandbits(256), 64) 
        com = hashing(key + msg)


        return (com,key)
    
def verify(msg,commitment,key):   
    return commitment == hashing(key + msg)

def hashing(value):
    #print(sha256(value.encode()).hexdigest())
    return sha256(value.encode()).hexdigest()




if __name__ == '__main__':
    commit,key = getCommitment("testing")
    hex_val = binascii.hexlify(commit.encode())
    a = int(hex_val,16)
    b = hex(a)[2:]
    c = bytes.fromhex(b)
    print(commit)
    print(hex_val)
    print(a)
    print(b)
    print(c.decode())
    
    
    
