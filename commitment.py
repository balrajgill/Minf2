from sys import argv
from hashlib import sha256
from random import getrandbits

def getCommitment(msg):
        key = "{0:0{1}x}".format(getrandbits(256), 64) 
        com = hashing(key + msg)


        return (com,key)
    
def verify(msg,commitment,key):   
    print(commitment == hashing(key + msg))

def hashing(value):
    #print(sha256(value.encode()).hexdigest())
    return sha256(value.encode()).hexdigest()