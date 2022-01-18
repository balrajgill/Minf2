import json
import commitment
from sys import addaudithook
from web3 import Web3
from web3.middleware import geth_poa_middleware
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from random import SystemRandom
from sys import argv
from hashlib import sha256
from random import getrandbits


infura_url = "https://rinkeby.infura.io/v3/6fca4c303dfc43a2b12e7da11b47e685"
add_main = "https://mainnet.infura.io/v3/6fca4c303dfc43a2b12e7da11b47e685"

web3 = Web3(Web3.HTTPProvider(infura_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

address = "0x51b8ec3F2123924Fec11C55C32AE6A6C162017d3"

abi = json.loads('[{"inputs": [],"name": "retrieve","outputs": [{"internalType": "string[]","name": "","type": "string[]"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "string","name": "num","type": "string"}],"name": "store","outputs": [],"stateMutability": "nonpayable","type": "function"}]')


contract_instance = web3.eth.contract(address=address, abi=abi)
print(contract_instance.functions.retrieve().call()[0])


