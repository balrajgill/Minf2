from base64 import b64encode
import binascii
from cgi import test
from functools import partial
import http
from logging import root
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from matplotlib.cbook import boxplot_stats
from kivy.uix.textinput import TextInput
from matplotlib.pyplot import text
from numpy import size
from web3 import Web3
import json
import tools.commitment as commitment
from tools import elgamalblind
import pickle
import requests
import socket
import httplib2
from binascii import hexlify, unhexlify
import ecdsa
import hashlib, secrets
import eth_abi

url = "http://127.0.0.1:5000/getAdminSignature"

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
web3.eth.default_account = web3.eth.accounts[0]
address = "0x911EEFA15bD58d016c9F87b2E84753D0AA29EF52"
abi = json.loads('[ { "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "Admin_yi", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "GetCurrentTime", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "string", "name": "key", "type": "string" }, { "internalType": "string", "name": "vote", "type": "string" }, { "internalType": "uint256", "name": "l", "type": "uint256" } ], "name": "ValidCommitment", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "Voter_xi", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "Voter_xi_bytes", "outputs": [ { "internalType": "bytes32", "name": "", "type": "bytes32" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "string", "name": "ballots", "type": "string" } ], "name": "addBallot", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "ballotList", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "countVotes", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "string", "name": "", "type": "string" } ], "name": "counts", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "emptyAll", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "gas", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "_b", "type": "uint256" }, { "internalType": "uint256", "name": "_e", "type": "uint256" }, { "internalType": "uint256", "name": "_m", "type": "uint256" } ], "name": "modExp", "outputs": [ { "internalType": "uint256", "name": "result", "type": "uint256" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "ri", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "seeBallotList", "outputs": [ { "internalType": "string[]", "name": "", "type": "string[]" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "bytes32", "name": "", "type": "bytes32" } ], "name": "sendKey", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "bytes32", "name": "bm", "type": "bytes32" }, { "internalType": "uint256", "name": "m", "type": "uint256" }, { "internalType": "uint256", "name": "ubsig", "type": "uint256" }, { "internalType": "uint256", "name": "r", "type": "uint256" } ], "name": "sendvote", "outputs": [], "stateMutability": "nonpayable", "type": "function" } ]')
contract_instance = web3.eth.contract(address=address, abi=abi)
votes = contract_instance.functions.seeBallotList().call()

for account in web3.eth.accounts:
    print(account)




ifile = open("keys/elgampub","rb")
pubkey = pickle.load(ifile)
ifile.close()


ifile = open("keys/sk","rb")
sk = pickle.load(ifile)
ifile.close()

print("------------------------------------")
print(pubkey[0])
print(pubkey[1])
print(pubkey[2])
print("------------------------------------")
test_floatie = FloatLayout()


vk = sk.get_verifying_key()
sig = sk.sign(b"message")
print(b64encode(sig))
a = vk.verify(sig, b"message") # True
print(a)

infile = open("keys/sk",'wb')
pickle.dump(sk,infile)
outfile = open("keys/vk","wb")
pickle.dump(vk,outfile)
infile.close()
outfile.close()
    



def select(drop_button, text, btn):
    drop_button.text = text
    currentSelectedVote = text
    f = open("tools/currentvote.txt", "w")
    f.write(text)
    f.close()


def output(inputbox,text):
    inputbox.text = "\n" + text



def chooseVote(drop_button,dropbutton2,inputbox, text, btn):
    f = open("tools/currentvote.txt", "r")
    a = f.read()
    f.close()
    vote = a.split(".")[0]
    

    
    commit,key = commitment.getCommitment(vote)
    m = int(hexlify(commit.encode()),16)
    print(m)
    k,r,h,blind_commit = elgamalblind.blind(commit,pubkey)
    data_to_send = str(blind_commit) + "-" + str(k) + "-" + str(r)
    signed_blind = int((requests.post("http://127.0.0.1:5000/getAdminSignature", data=data_to_send)).text)
    print("in app signed:" + str(signed_blind))
    y = elgamalblind.unblind(signed_blind,pubkey,k,r,h,blind_commit)
    print(f'ubsig is : {y}')
    print(f"r is : {r}")
    ecommit = commit.encode("utf-8")
    print(ecommit)
    elgamalblind.verefy(m,y,pubkey,r)
    contract_instance.functions.sendvote(commit.encode(),m,y,r).transact()
    aa = contract_instance.functions.ValidCommitment(key,vote,0).call()
    print("========================================================================" + str(aa))
    print(f"r is : {r}")
    #k,r,h,blindmsg=blind(msg,pubkey)
    #ubsig = unblind(sig,pubkey,k,r,h,blindmsg)
    #print(f'ubsig is : {ubsig}')
    #verefy(m,ubsig,pubkey,r)
    output(inputbox,commit)
    output(inputbox,str(blind_commit))


    drop_button.text = f"You Selected {a}"
    drop_button.disabled = True
    dropbutton2.disabled = True
    
    
dropButton = Button(text="Select Vote", size_hint=(0.25, 0.15),pos_hint={"x":0.07, "top":0.4})

# Create a drop down
dropdown = DropDown()

for index in range(len(votes)):
    # Creating our button
    btn = Button(text=f"{index+1}. {votes[index]} ", size_hint_y=None, height=44)
    btn.bind(on_release=partial(select, dropButton, btn.text))
    btn.bind(on_release=dropdown.dismiss)
    dropdown.add_widget(btn)

# Binding the button to a function that triggers the drop down
dropButton.bind(on_release=dropdown.open)

test_floatie.add_widget(dropButton)

dropButton1 = Button(text="Confirm Vote", size_hint=(0.25, 0.15), pos_hint={"x":0.37, "top":0.4})
dropButton2 = Button(text="Send Key", size_hint=(0.25, 0.15),pos_hint={"x":0.67, "top":0.4})
dropButton3 = Button(text="Display data", size_hint=(0.25, 0.15),pos_hint={"x":0.67, "top":0.2})
dropButton4 = Button(text="Get Results", size_hint=(0.25, 0.15),pos_hint={"x":0.37, "top":0.2})



textinput = TextInput(text='1. Click Select Vote to open list of ballots you can vote for, from the list pick your ballot and then press confirm after which vote is cast')
textinput.size_hint = (0.8,0.3)
textinput.pos_hint = {"x":0.1,"top":0.8}
test_floatie.add_widget(textinput)

dropButton1.bind(on_release=partial(chooseVote, dropButton,dropButton1,textinput, ""))
test_floatie.add_widget(dropButton1)
test_floatie.add_widget(dropButton2)
test_floatie.add_widget(dropButton3)
test_floatie.add_widget(dropButton4)
# Running la app
class MainApp(App):
    def build(self):
        return test_floatie


MainApp().run()