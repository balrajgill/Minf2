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


ifile = open("keys/admin_pub","rb")
pubkey = pickle.load(ifile)
ifile.close()
ifile = open("keys/admin_priv","rb")
privkey = pickle.load(ifile)
ifile.close()


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

#admin_signed_vote = int((requests.post("http://127.0.0.1:5000/getAdminSignature", data=str(blind_commit))).text)


















#test on this side
sig = blindsignature.signature(blind_commit, privkey)

ubsig = blindsignature.unblind(sig,r,pubkey)
verified = blindsignature.verify(ubsig,r,pubkey)
msg2 = bytes.fromhex(hex(verified)[2:])

print(f"msg is: {commit}")
print(f"blind msg is: {str(blind_commit)[0:50]}")
print(f"signature is: {str(sig)[0:50]}")
print(f"unblinded signature is: {str(ubsig)[0:50]}")
print(f"verified is: {str(verified)[0:50]}")
print(f'b is: {msg2}')








