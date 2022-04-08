from cgi import test
from functools import partial
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
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
web3.eth.default_account = web3.eth.accounts[0]
address = "0x7f341a2488a1d274205470a206612A316a96114f"
abi = json.loads('[ { "inputs": [ { "internalType": "string", "name": "ballots", "type": "string" } ], "name": "addBallot", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "getVoteList", "outputs": [ { "internalType": "string[]", "name": "", "type": "string[]" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "seeBallotList", "outputs": [ { "internalType": "string[]", "name": "", "type": "string[]" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "string", "name": "vote", "type": "string" } ], "name": "sendvote", "outputs": [], "stateMutability": "nonpayable", "type": "function" } ]')
contract_instance = web3.eth.contract(address=address, abi=abi)
votes = contract_instance.functions.seeBallotList().call()

ifile = open("keys/elgampub","rb")
pubkey = pickle.load(ifile)
ifile = open("keys/elgampriv","rb")
privkey = pickle.load(ifile)


test_floatie = FloatLayout()

def select(drop_button, text, btn):
    drop_button.text = text
    currentSelectedVote = text
    print("select "+currentSelectedVote)
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
    print(vote)
    commit,key = commitment.getCommitment(vote)
    k,r,h,blindmsg= elgamalblind.blind(commit,pubkey)

    
    output(inputbox,commit)
    output(inputbox,str(blindmsg))

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
dropButton2 = Button(text="Extra Stuff", size_hint=(0.25, 0.15),pos_hint={"x":0.67, "top":0.4})


textinput = TextInput(text='1. Click Select Vote to open list of ballots you can vote for, from the list pick your ballot and then press confirm after which vote is cast')
textinput.size_hint = (0.8,0.3)
textinput.pos_hint = {"x":0.1,"top":0.8}
test_floatie.add_widget(textinput)

dropButton1.bind(on_release=partial(chooseVote, dropButton,dropButton1,textinput, ""))
test_floatie.add_widget(dropButton1)
test_floatie.add_widget(dropButton2)
# Running la app
class MainApp(App):
    def build(self):
        return test_floatie


MainApp().run()