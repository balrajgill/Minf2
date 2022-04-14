import json
import requests
import pickle
from web3 import Web3
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from random import SystemRandom, random
from sys import argv
import Crypto.Hash.MD5 as MD5
import Crypto.Signature 
from encodings import utf_8
from hmac import digest
from Crypto.Signature import PKCS1_v1_5
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA384
from binascii import hexlify, unhexlify
from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
from ellipticcurve.signature import Signature
from random import getrandbits


ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
web3.eth.default_account = web3.eth.accounts[1]
address = "0xF1555bE0CB65226AdE1940b7986310391735A9d9"
abi = json.loads('[ { "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "Admin_yi", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "Voter_xi", "outputs": [ { "internalType": "bytes32", "name": "", "type": "bytes32" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "a", "outputs": [ { "internalType": "bytes32", "name": "", "type": "bytes32" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "b", "outputs": [ { "internalType": "bytes16", "name": "", "type": "bytes16" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "counts", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "emptyAll", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "_b", "type": "uint256" }, { "internalType": "uint256", "name": "_e", "type": "uint256" }, { "internalType": "uint256", "name": "_m", "type": "uint256" } ], "name": "modExp", "outputs": [ { "internalType": "uint256", "name": "result", "type": "uint256" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "seeBallotList", "outputs": [ { "internalType": "string[]", "name": "", "type": "string[]" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "string", "name": "key", "type": "string" }, { "internalType": "string", "name": "vote", "type": "string" }, { "internalType": "uint256", "name": "i", "type": "uint256" } ], "name": "sendKey", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "bytes32", "name": "xi", "type": "bytes32" }, { "internalType": "uint256", "name": "m", "type": "uint256" }, { "internalType": "uint256", "name": "ubsig", "type": "uint256" }, { "internalType": "uint256", "name": "r", "type": "uint256" } ], "name": "sendvote", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "", "type": "address" } ], "name": "voter_blind_verified", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "", "type": "address" } ], "name": "voter_vote_verified", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "stateMutability": "view", "type": "function" } ]')
contract_instance = web3.eth.contract(address=address, abi=abi)

key = "db8800082e4764934a006573b1c831ff5cad2e0d13de81fdf200c82f0fc67ee1"
m = "2"


costs = []

#e = contract_instance.functions.sendKey(key,m,1).estimateGas()
#print(e)

key = "666fe3bb9d0a1dedb434ad3448ad60fc2f676fc95578139f136b8d5d150ce0e8"
xi = "d7ceabc86f5b3fe27d01ed9ad2a59841"





for i in range(100):
    key = "{0:0{1}x}".format(getrandbits(256), 64)
            #print(key) 
    
    com = Web3.soliditySha3(['string'], [key+"1"])
    com = (com.hex()[2:])[:32]
    msg = int(hexlify(com.encode()),16)
    ub = getrandbits(128)
    r = getrandbits(128)

    e2 = contract_instance.functions.sendvote(bytes(com,"utf-8"),msg,ub,r).estimateGas()
    print(e2)

