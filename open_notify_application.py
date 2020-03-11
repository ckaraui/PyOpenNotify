''' This code allows to retrieve data from Open Notify API,
 display data in the PyQt, and stores the retrieved data into MongoDB'''
import sys
from functools import partial
from PyQt5 import QtWidgets
import pymongo
import requests

GLOBAL_MESSAGE_ERROR = "Error"


class PyOpenNotifyView(QtWidgets.QMainWindow):
    ''' This class presents the View'''

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Open Notify')
        self.setFixedSize(435, 435)
        self.general_layout = QtWidgets.QVBoxLayout()
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.general_layout)
        self.create_display()
        self.create_buttons()

    def create_display(self):
        ''' This function allows to create the edit text in the view'''
        form_layout = QtWidgets.QFormLayout()
        self.display1 = QtWidgets.QLineEdit()
        self.display2 = QtWidgets.QLineEdit()
        self.display3 = QtWidgets.QLineEdit()
        self.display4 = QtWidgets.QLineEdit()
        form_layout.addRow('crafts: ', self.display1)
        form_layout.addRow('names: ', self.display2)
        form_layout.addRow('message: ', self.display3)
        form_layout.addRow('number: ', self.display4)
        self.general_layout.addLayout(form_layout)

    def  create_buttons(self):
        ''' This function allows to create the buttons in the view'''
        self.buttons = {}
        layout = QtWidgets.QVBoxLayout()
        self.buttons['data about astronauts currently in ' \
                     'space'] = \
            QtWidgets.QPushButton('Get data about astronauts currently in space')
        layout.addWidget(self.buttons['data about astronauts currently in space'])
        self.general_layout.addLayout(layout)

    def set_display_text(self, result_model):
        ''' This function display the retrieved data from model into view'''
        self.display1.setText(str(result_model[0]))
        self.display2.setText(str(result_model[1]))
        self.display3.setText(str(result_model[2]))
        self.display4.setText(str(result_model[3]))

def listtostring(in_list=""):
    ''' This function modifies a list into string'''
    str1 = ", "
    return str1.join(in_list)


class PyOpenNotifyCtrl:
    ''' This class presents the Controller'''

    def __init__(self, view, model):
        self.window = view
        self.model = model
        self.connectclick()

    def displayexpression(self, event=None):
        ''' This function allows to retrieve data from the model'''
        result_model = self.model()
        if result_model != GLOBAL_MESSAGE_ERROR:
            self.window.set_display_text(result_model)

    def connectclick(self):
        ''' This function permits to connect the button
        to the function self.displayexpression when a click event is handled'''
        self.window.buttons['data about astronauts currently in space'].clicked.connect\
            (partial(self.displayexpression, ''))

def retrievedata():
    ''' This function presents the Model'''
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
        result = [listtostring(crafts), listtostring(names), message, number]
    except:
        return GLOBAL_MESSAGE_ERROR
    return result

if __name__ == '__main__':
    APP = QtWidgets.QApplication(sys.argv)
    WINDOW = PyOpenNotifyView()
    PyOpenNotifyCtrl(view=WINDOW, model=retrievedata)
    WINDOW.show()
    sys.exit(APP.exec_())
