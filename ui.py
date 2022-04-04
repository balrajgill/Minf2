from turtle import pos
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.app import App
import vote1
# create a dropdown with 10 buttons



class MainClass(App):
    
    dropdown = DropDown()
    votes = vote1.getVotes()
    for index in range(len(votes)):
      
        btn = Button(text= f'{index+1}. {votes[index]}', size_hint_y=None, height=44)
        btn.bind(on_release=lambda btn: dropdown.select(btn.text))
 


        # then add the button inside the dropdown
        dropdown.add_widget(btn)
        
        # create a big main button
    mainbutton = Button(text='Select Vote', size_hint=(None, None))

    def chooseVote(x):
        setattr(mainbutton, 'text', x)
        print(x)

    #mainbutton.bind(on_release=dropdown.open)


    #dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
    #dropdown.bind(on_select=lambda instance, x: chooseVote(x))

    #dropdown.bind(on_select=lambda instance, x: print(vote1.getVotes()))
    btn1 = Button(text='Hello world 1', pos = (500,500))

if __name__ == '__main__':
    MainClass().run()