import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import main

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Voting'
        self.left = 500
        self.top = 500
        self.width = 800
        self.height = 500
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create textbox
        self.textbox1 = QLineEdit(self)
        self.textbox1.move(200, 10)
        self.textbox1.resize(400,300)

        self.VoteList = QListWidget(self)
        self.VoteList.move(600, 10)
        self.VoteList.resize(120,300)
        
        # Create a button in the window
        buttonGetVote = QPushButton('Get Ballots', self)
        buttonGetVote.move(200,320)
      

        buttonSelectVote = QPushButton('Select Vote', self)
        buttonSelectVote.move(350,320)

        buttonStuff = QPushButton('Stuff', self)
        buttonStuff.move(500,320)
        
        # connect button to function on_click
        buttonGetVote.clicked.connect(self.on_click_GetVote)
        buttonSelectVote.clicked.connect(self.on_click_SelectVote)
        buttonStuff.clicked.connect(self.on_click_Stuff)
        self.show()
    
    @pyqtSlot()
    def on_click_GetVote(self):
        textboxValue = self.textbox1.text()
        votes = main.getVotes()
        for i in range(len(votes)):
            self.VoteList.insertItem(i, str(i+1) + ". " + votes[i])
    
    def on_click_SelectVote(self):
        textboxValue = self.textbox1.text()
        self.textbox1.setText("")
   
    def on_click_Stuff(self):
        textboxValue = self.textbox1.text()
        self.textbox1.setText("")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())