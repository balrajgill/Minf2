import json
import requests
import pickle
import tools.blindsignature as blindsignature
import tools.commitment as commitment
from web3 import Web3
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from random import SystemRandom
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


ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
web3.eth.default_account = web3.eth.accounts[1]


address = "0x31C94C8ED6f9919F088C5a5F975D3Ffa5D25C053"


abi = json.loads('[ { "inputs": [ { "internalType": "string", "name": "ballots", "type": "string" } ], "name": "addBallot", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "getVoteList", "outputs": [ { "internalType": "string[]", "name": "", "type": "string[]" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "seeBallotList", "outputs": [ { "internalType": "string[]", "name": "", "type": "string[]" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "string", "name": "vote", "type": "string" } ], "name": "sendvote", "outputs": [], "stateMutability": "nonpayable", "type": "function" } ]')
contract_instance = web3.eth.contract(address=address, abi=abi)
pubkey, privkey = blindsignature.keygen(2 ** 512)
votes = []




def getVotes():
    ballots_choices = contract_instance.functions.seeBallotList().call()
    return ballots_choices

def get_commit_Vote(vote):
    
    commit_choice = commitment.getCommitment(vote)
    return commit_choice



def SignVote(msg):
    msg = str(msg)
    privateKey = PrivateKey()
    publicKey = privateKey.publicKey()
    # Generate Signature
    signature = Ecdsa.sign(msg, privateKey)
    #a = signature.toBase64()
    # To verify if the signature is valid
    #print(Ecdsa.verify(msg, Signature.fromBase64(a), publicKey))
    return(signature.toBase64())


votes = getVotes()
commit,key = get_commit_Vote(votes[0])
r,blind_commit=blindsignature.blind(commit,pubkey)
signed_vote = SignVote(blind_commit)
r = requests.post("http://127.0.0.1:5000", data=signed_vote)
#Alice receives the blind message and signs ita

#this should be done by admin signing the blinded message after checking voter is legit
# signature of the ballot
sig = blindsignature.signature(blind_commit, privkey)
#Bob recieves the signed message and unblinds it
"""ubsig = blindsignature.unblind(sig,r,pubkey)
#verifier verefies the message
verified = blindsignature.verify(ubsig,r,pubkey)
msg2 = bytes.fromhex(hex(verified)[2:])

print("msg is:" + " " + commit)
print(f'b is: {msg2}')
"""








