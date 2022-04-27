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
import re

url = "http://127.0.0.1:5000/getAdminSignature"


abi_text = ""
with open("tools/abi.txt","r") as abi_text_file:
    abi_text = re.sub(r"[\n\t\s]*", "", (abi_text_file.read()))

print(abi_text)
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
web3.eth.default_account = web3.eth.accounts[0]
address = "0xA8F607484292fF880482BEc719c0A095aF87E754"
abi = json.loads(abi_text)
contract_instance = web3.eth.contract(address=address, abi=abi)
votes = contract_instance.functions.seeBallotList().call()



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
a = vk.verify(sig, b"message") # True

infile = open("keys/sk",'wb')
pickle.dump(sk,infile)
outfile = open("keys/vk","wb")
pickle.dump(vk,outfile)
infile.close()
outfile.close()
    



def select(drop_button, text, btn):
    drop_button.text = text
    currentSelectedVote = text
    f = open("tools/currentvote1.txt", "w")
    f.write(text)
    f.close()


def output(inputbox,text):
    inputbox.text = "\n" + text


def display():
    display = "here here here here here here here here"

def sendKey(a,b):

    f = open("voterdata/currentvote1.txt", "r")
    v = f.read()
    f.close()
    f = open("voterdata/key1.txt", "r")
    k = f.read()
    f.close()
    print("key from sdfyasduhfj is:" + str(k))
    contract_instance.functions.sendKey(k,v,1).transact()
    b.disabled = True


def chooseVote(drop_button,dropbutton2,inputbox, text, btn):
    f = open("voterdata/currentvote1.txt", "r")
    a = f.read()
    f.close()
    vote = a.split(".")[0]
    
    
    commit,key = commitment.getCommitment(vote)

    f = open("voterdata/key1.txt", "w")
    f.write(key)
    f.close()




    m = int(hexlify(commit.encode()),16)
    print("m is :" + str(m))
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
    contract_instance.functions.sendvote(m,y,r).transact()

    print(f"r is : {r}")
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
dropButton2.bind(on_release=partial(sendKey,dropButton2))

test_floatie.add_widget(dropButton1)
test_floatie.add_widget(dropButton2)
test_floatie.add_widget(dropButton3)
test_floatie.add_widget(dropButton4)
# Running la app
class MainApp(App):
    def build(self):
        return test_floatie


MainApp().run()