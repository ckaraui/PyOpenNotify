import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QLabel, QWidget,QMainWindow, QLineEdit, QHBoxLayout, QFormLayout
from PyQt5.QtCore import Qt
from functools import partial
import pymongo
import requests
import json

globalMessageError="Error"

class PyOpenNotifyView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Open Notify')
        self.setFixedSize(435, 435)
        self.generalLayout = QVBoxLayout()
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.generalLayout)
        self.createDisplay()
        self.createButtons()

    def createDisplay(self):
        formLayout = QFormLayout()
        self.display1=QLineEdit()
        self.display2=QLineEdit()
        self.display3=QLineEdit()
        self.display4=QLineEdit()
        formLayout.addRow('crafts:', self.display1)
        formLayout.addRow('names:', self.display2)
        formLayout.addRow('message:', self.display3)
        formLayout.addRow('number:', self.display4)
        self.generalLayout.addLayout(formLayout)

    def  createButtons(self):
        self.buttons = {}
        layout = QVBoxLayout()
        self.buttons['data about astronauts currently in space'] = QPushButton('Get data about astronauts currently in space')
        layout.addWidget(self.buttons['data about astronauts currently in space'])
        self.generalLayout.addLayout(layout)

    def setDisplayText(self, resultModel):
        self.display1.setText(str(resultModel[0]))
        self.display2.setText(str(resultModel[1]))
        self.display3.setText(str(resultModel[2]))
        self.display4.setText(str(resultModel[3]))


def listToString(s):
    str1 = ", "
    return (str1.join(s))

class PyOpenNotifyCtrl:
    def __init__(self, window,model):
        self.window = window
        self.model=model
        self.connectClick()

    def displayExpression(self, event):
        resultModel=self.model()
        if resultModel != globalMessageError:
            self.window.setDisplayText(resultModel)

    def connectClick(self):
        self.window.buttons['data about astronauts currently in space'].clicked.connect(partial(self.displayExpression, ''))

def retrieveData():
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["mydatabase"]
        mycol = mydb["astros"]
        html = requests.get("http://api.open-notify.org/astros.json")
        data = html.json()
        mycol.insert_one(data)
        crafts = []

        names = []
        for i in range(0, len(data['people'])):
            crafts.append(data['people'][i]['craft'])
            names.append(data['people'][i]['name'])
        message = data['message']
        number = data['number']
        result = [listToString(crafts), listToString(names), message, number]
    except:
        return  globalMessageError
    return result

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PyOpenNotifyView()
    PyOpenNotifyCtrl(window=window,model=retrieveData)
    window.show()
    sys.exit(app.exec_())