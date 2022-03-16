from random import randrange, random
from collections import namedtuple
from math import log, gcd
from binascii import hexlify, unhexlify
import pickle
from flask import Flask,request

from tools import blindsignature
  

app = Flask(__name__)

#pubkey, privkey = blindsignature.keygen(2 ** 512)
ifile = open("keys/admin_pub","rb")
pubkey = pickle.load(ifile)
ifile.close()
ifile = open("keys/admin_priv","rb")
privkey = pickle.load(ifile)
ifile.close()
print(pubkey)
@app.route('/')

def hello_world():
    return 'main page adhfghfghfghsmin'


@app.route('/getAdminSignature',methods = ['POST', 'GET'])

def adminSignature():
    print("triggered")
    blind_commit = int(request.data)
    print(blind_commit)
    blind_commit_signed = blindsignature.signature(blind_commit, privkey)
    print(blind_commit_signed)
    return str(blind_commit_signed)
  



# main driver function
if __name__ == '__main__':
  

    app.run()

   