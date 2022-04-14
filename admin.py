from random import randrange, random
from collections import namedtuple
from math import log, gcd
from binascii import hexlify, unhexlify
import pickle
from flask import Flask,request
from regex import R

from tools import blindsignature
from tools import elgamalblind
  

app = Flask(__name__)

#pubkey, privkey = blindsignature.keygen(2 ** 512)


"""infile = open("keys/admin_priv",'wb')
pickle.dump(pubkey,infile)
outfile = open("keys/admin_priv","wb")
pickle.dump(privkey,outfile)
infile.close()
outfile.close()
"""
ifile = open("keys/elgampub","rb")
pubkey = pickle.load(ifile)
ifile.close
ifile = open("keys/elgampriv","rb")
privkey = pickle.load(ifile)
ifile.close()

ifile = open("keys/vk","rb")
vk = pickle.load(ifile)
ifile.close()

#print(pubkey)

@app.route('/')

def hello_world():
    return 'main page adhfghfghfghsmin'


@app.route('/getAdminSignature',methods = ['POST', 'GET'])

def adminSignature():

    #ata_to_send = str(blind_commit) + "-" + str(k) + "-" + str(r)
    print("triggered")
    split = ((request.data).decode("utf-8")).split("-")
    print(split)
    blind_commit = int(split[0])
    k = int(split[1])
    r = int(split[2])

    #print(blind_commit)
    blind_commit_signed = elgamalblind.signature(blind_commit, privkey,k,r)
    print("in admin blind signed:" + str(blind_commit_signed))
    return str(blind_commit_signed)
  



# main driver function
if __name__ == '__main__':
  

    app.run()

   