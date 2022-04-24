from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QLabel, QTextEdit 
import sys 

class WelcomeScreen(QMainWindow):
    def __init__(self):
        #default instance
        super(WelcomeScreen, self).__init__()

        #load the UI file
        loadUi("welcome.ui", self)

        #define widgets
        self.bt_xlsx = self.findChild(QPushButton, "bt_spreadsheet")
        self.bt_pdf = self.findChild(QPushButton, "bt_pdf")


        #give functionality to button
        self.bt_xlsx.clicked.connect(self.gotoBrowseScreen)
        self.bt_pdf.clicked.connect(self.gotoBrowseScreen)

        #show the app
        # self.show()

    def gotoBrowseScreen(self):
        browse = BrowseScreen()
        widget.addWidget(browse)
        widget.setCurrentIndex(widget.currentIndex()+1)
        loadUi("browse.ui",self)                  

class BrowseScreen(QMainWindow):
    def __init__(self):
            #default instance
            super(BrowseScreen, self).__init__()

            #load the UI file
            loadUi("browse.ui", self)

            #define widgets
            self.bt_back = self.findChild(QPushButton, "bt_back")
            self.bt_browsefile = self.findChild(QPushButton, "bt_browsefile")
            self.bt_upload = self.findChild(QPushButton, "bt_upload")

            #give functionality to button
            self.bt_back.clicked.connect(self.gotoWelcomeScreen)
            self.bt_browsefile.clicked.connect(self.browse_file)      
            self.bt_upload.clicked.connect(self.gotoUrlScreen)

            #show the app
            # self.show()


    def gotoUrlScreen(self):
        url = URLScreen()
        widget.addWidget(url)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def browse_file(self):
        print("In Browse File function")

    def gotoWelcomeScreen(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)        

class URLScreen(QMainWindow):
    def __init__(self):
            #default instance
            super(URLScreen, self).__init__()

            #load the UI file
            loadUi("url.ui",self)

            #define widgets
            self.bt_back = self.findChild(QPushButton, "bt_back")
            self.bt_submit = self.findChild(QPushButton, "bt_submit")

            #give functionality to button
            self.bt_back.clicked.connect(self.gotoBrowseScreen)    
            self.bt_submit.clicked.connect(self.gotoElementScreen)

            #show the app
            # self.show()

    def gotoBrowseScreen(self):
        browse = BrowseScreen()
        widget.addWidget(browse)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def gotoElementScreen(self):
        element = ElementsScreen()
        widget.addWidget(element)
        widget.setCurrentIndex(widget.currentIndex()+1)
        

class ElementsScreen(QMainWindow):
    def __init__(self):
            #default instance
            super(ElementsScreen, self).__init__()

            #load the UI file
            loadUi("element.ui",self)

            #define widgets
            self.bt_back = self.findChild(QPushButton, "bt_back")
            self.bt_submit = self.findChild(QPushButton, "bt_submit")

            #give functionality to button
            self.bt_back.clicked.connect(self.gotoUrlScreen)    
            self.bt_submit.clicked.connect(self.gotoNextScreen)

            #show the app
            # self.show()

    def gotoUrlScreen(self):
        url = URLScreen()
        widget.addWidget(url)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def gotoNextScreen(self):
        print("In Browse File function")   

    # def ElementsScreen(self):
    #     uic.loadUi("elements.ui",self)   
    #     
   

#main / show the app
width = 801
height = 663

app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(height)
widget.setFixedWidth(width)
widget.resize(width, height)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
