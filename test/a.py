from cgi import test
from functools import partial
from logging import root
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from matplotlib.cbook import boxplot_stats
import vote1
test_floatie = BoxLayout()
test_floatie.padding = 30
test_floatie.spacing = 20

def select(drop_button, text, btn):
    drop_button.text = text



dropButton = Button(text="Select Vote", size_hint=(0.7, 0.2))

# Create a drop down
dropdown = DropDown()
votes = vote1
for index in range(10):
    # Creating our button
    btn = Button(text="Option " + str(index), size_hint_y=None, height=44)
    btn.bind(on_release=partial(select, dropButton, btn.text))
    btn.bind(on_release=dropdown.dismiss)
    dropdown.add_widget(btn)

# Binding the button to a function that triggers the drop down
dropButton.bind(on_release=dropdown.open)

test_floatie.add_widget(dropButton)
dropButton1 = Button(text="Confirm Vote", size_hint=(0.7, 0.2))
dropButton2 = Button(text="Extra Stuff", size_hint=(0.7, 0.2))

test_floatie.add_widget(dropButton1)
test_floatie.add_widget(dropButton2)
# Running la app
class MainApp(App):
    def build(self):
        return test_floatie


MainApp().run()