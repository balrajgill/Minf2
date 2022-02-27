import json
from PySide6 import os
from torch import sign
import blindsignature
import commitment
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
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA384


ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
web3.eth.default_account = web3.eth.accounts[0]
address = "0x06F1eDf77f35B89722aBF3526f3441128B874F37"
elibility_list = ["0x7AA44Ae701d54F1f400F13d9680B55EdafD51033","0x532d8c9030242249a05CFFC5c8fa4363273AC05d","0x5E81235FbEF5f2f0975859F794ceEf6B47825eCA"]

abi = json.loads('[ { "inputs": [ { "internalType": "string", "name": "ballots", "type": "string" } ], "name": "addBallot", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "getVoteList", "outputs": [ { "internalType": "string[]", "name": "", "type": "string[]" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "seeBallotList", "outputs": [ { "internalType": "string[]", "name": "", "type": "string[]" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "string", "name": "vote", "type": "string" } ], "name": "sendvote", "outputs": [], "stateMutability": "nonpayable", "type": "function" } ]')
contract_instance = web3.eth.contract(address=address, abi=abi)

def getVotes():
    ballots_choices = contract_instance.functions.seeBallotList().call()
    print(ballots_choices)
    choice = ballots_choices[0]
    commit_choice = commitment.getCommitment(choice)[0]
    #print(commit_choice)
    commit_choice_hash = MD5.new(commit_choice.encode()).digest()
    return ballots_choices

pub_voter_key_plain = b'-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDaKWHuxVQhSieMX3KJHIZnfohZ\n8M0DDIrIFLPq8YKtGkcd1VR1D9i/Ary8+YP4kyyoFrnO6HfNFllNkXtVCzGYKuO1\nzTGZisY9pojzm5cJd5SrHwaAhym8YqVgFBtpMxH29NrjMytyHV+eWKTHdqtYVVnp\nUEJVpI3eDb9YweoLPwIDAQAB\n-----END PUBLIC KEY-----'
priv_voter_key_plain = b'-----BEGIN RSA PRIVATE KEY-----\nMIICXgIBAAKBgQDaKWHuxVQhSieMX3KJHIZnfohZ8M0DDIrIFLPq8YKtGkcd1VR1\nD9i/Ary8+YP4kyyoFrnO6HfNFllNkXtVCzGYKuO1zTGZisY9pojzm5cJd5SrHwaA\nhym8YqVgFBtpMxH29NrjMytyHV+eWKTHdqtYVVnpUEJVpI3eDb9YweoLPwIDAQAB\nAoGADD0apxTEBJ6lgDAxcm+xg7X47fdVdq5TKIQJ895/d11sT+y2sV8TWuPdkG6z\nlS9+wvz6P4b/qGUnbWFvZmKJO1Rygj86KUvIQYnSCikAbwwzO1K54fm3Ia4H5Jvv\ne+I0R+hC9itKBWsgLd9T3BNVwZx/R942epu4zWyxM492ZoECQQDg2svQooxlknqH\ni0av35tvtKM+A4RtZ5JZIbdyu7zT8Tty1y//F7jItswLd2+cP/1HhQ4JFraq69qh\nfOQpqpXHAkEA+GFBj0+DJHUfXZuZDayu9iE83EW9s0P0/2DHen5nGfa6UPRKrl/A\nIl/wViDZ8EFQExndSGZKtW+4ZZdYxqn+yQJBAIxvmwR/wXhe+DBYCJon6ojmJV7C\nC5/ZJEqPCGicYN9ut1aOl+eXBU42/VHcEtVgEeztaUq76PLvw+lAe7CaXlkCQQDO\nuJtI/GNop3Y4gXUsFWn0/graRc0x80BogBLmF2gWCuxczkWNxbFyqqir9mGM/b74\ndtFeHYzWXyp4mzNO/VNJAkEAiDOjplZDO5vAQs9Qw2etQDjxHwiYa/0ix26zzFSB\n81Xa9jMMmQ02J7FPhg+FK5S3Zs1taO6oCipLFHvYzEtX1A==\n-----END RSA PRIVATE KEY-----'
public_key = RSA.importKey(pub_voter_key_plain)
priv_key = RSA.importKey(priv_voter_key_plain)


def SignVote():
    


    msg = "plain text message test"
    msg2 = "plain text message test"
    digest = SHA384.new()
    digest.update(msg.encode('utf_8'))

    signer = PKCS1_v1_5.new(priv_key)
    sig = signer.sign(digest)
    #print(sig.hex())

    digest2 = SHA384.new()
    digest2.update(msg2.encode('utf_8'))

    verifier = PKCS1_v1_5.new(public_key)
    valid = verifier.verify(digest2,sig)

    print(valid)

getVotes()
SignVote()


blindmsg = blindsignature.blind("testing", public_key)



#contract_instance.functions.sendvote(str(commit_choice_hash)).transact()
#votes = contract_instance.functions.getVoteList().call()
#print(votes)







