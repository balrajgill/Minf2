from random import randrange, random
from collections import namedtuple
from math import log, gcd
from binascii import hexlify, unhexlify
import pickle
from flask import Flask,request

from tools.blindsignature import blind
  

app = Flask(__name__)
  

@app.route('/')

def hello_world():
    return 'main page admin'


@app.route('/getAdminSignature',methods = ['POST', 'GET'])

def adminSignature():

    blind_sig = request.form['msg']
    return blind_sig
  



# main driver function
if __name__ == '__main__':
  

    app.run()

   