from msilib.schema import Class
from turtle import position
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegExp, QObject, QCoreApplication
from PyQt5.QtGui import QValidator, QRegExpValidator 
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QFileDialog, QDialog, QLineEdit, QPushButton, QLabel, QTextEdit

from collections import OrderedDict
from PyPDF2 import PdfFileReader
import sys 
import os
import time

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
        self.bt_xlsx.clicked.connect(self.gotopdfBrowseScreen)
        self.bt_pdf.clicked.connect(self.gotopdfBrowseScreen)

        #show the app
        # self.show()

    #go to the next menu
    def gotopdfBrowseScreen(self):
        browse = pdfBrowseScreen()
        widget.addWidget(browse)
        widget.setCurrentIndex(widget.currentIndex()+1)
        loadUi("browse.ui",self)            

class pdfBrowseScreen(QMainWindow):
    def __init__(self):
            #default instance
            super(pdfBrowseScreen, self).__init__()

            #load the UI file
            loadUi("browse.ui", self)

            #define widgets
            self.bt_back = self.findChild(QPushButton, "bt_back")

            self.bt_browsefile = self.findChild(QPushButton, "bt_browsefile")
            self.le_file_name = self.findChild(QLineEdit, "le_file_name")

            self.bt_browsefile_1 = self.findChild(QPushButton, "bt_browsefile_1")
            self.le_file_name_1 = self.findChild(QLineEdit, "le_file_name_1")

            self.bt_browsefile_2 = self.findChild(QPushButton, "bt_browsefile_2")
            self.le_file_name_2 = self.findChild(QLineEdit, "le_file_name_2")

            self.bt_upload = self.findChild(QPushButton, "bt_upload")

            #give functionality to button
            self.bt_back.clicked.connect(self.gotoWelcomeScreen)
            self.bt_browsefile.clicked.connect(self.browse_file)
            self.bt_browsefile_1.clicked.connect(self.browse_file_1)
            self.bt_browsefile_2.clicked.connect(self.browse_file_2)
            self.bt_upload.clicked.connect(self.gotofinishScreen)

            #show the app
            # self.show()

    #go to the next menu
    def gotofinishScreen(self):
        #Check if user actually choose a file to upload, cannot proceed without doing so.
        if ((str(self.file_name[0]).find('.html') != -1) and (str(self.file_name_1[0]).find('.ini') != -1) and (str(self.file_name_2[0]).find('.ini') != -1)):
            finish = FinishScreen()
            widget.addWidget(finish)
            widget.setCurrentIndex(widget.currentIndex()+1) 
            self.execute(sys.argv)   
        else:
            print(str(self.file_name[0]).find('.html'))
            self.le_file_name.setText('Please choose the appropriate file to proceed')
            print(str(self.file_name_1[0]).find('.html'))
            self.le_file_name_1.setText('Please choose the appropriate file to proceed')
            print(str(self.file_name[0]).find('.html'))
            self.le_file_name_2.setText('Please choose the appropriate file to proceed')
    
    #open file dialog and allow selection of .html files only   
    def browse_file(self):
        print("In Browse .html File function")
        self.file_name = QFileDialog.getOpenFileName(self, 'Browse .html file: ', '', 'Resource Files (*.html)')
    
        #Output file name to label
        if self.file_name:
            self.le_file_name.setText(str(self.file_name[0]))
            print("\n \n HTML FILE NAME HERE !!!: " + (self.file_name[0]))

        #open file dialog and allow selection of .html files only   
    def browse_file_1(self):
        print("In Browse .ini_1 File function")
        self.file_name_1 = QFileDialog.getOpenFileName(self, 'Browse .ini file: ', '', 'Configuration file (*.ini)')
    
        #Output file name to label
        if self.file_name_1:
            self.le_file_name_1.setText(str(self.file_name_1[0]))
            print("\n \n .ini_1 FILE NAME HERE !!!: " + (self.file_name_1[0]))
    
            #open file dialog and allow selection of .html files only   
    def browse_file_2(self):
        print("In Browse .ini_2 File function")
        self.file_name_2 = QFileDialog.getOpenFileName(self, 'Browse .ini file: ', '', 'Configuration file (*.ini)')
    
        #Output file name to label
        if self.file_name_2:
            self.le_file_name_2.setText(str(self.file_name_2[0]))
            print("\n \n .ini_2 FILE NAME HERE !!!: " + (self.file_name_2[0]))


    #go back to the previous menu
    def gotoWelcomeScreen(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)        

    # Get each form field from the pdf file 
    # and store it in a ordered dictionary  
    def _getFields(self, obj, tree=None, retval=None, fileobj=None):
        fieldAttributes = {'/FT': 'Field Type', '/Parent': 'Parent', '/T': 'Field Name', '/TU': 'Alternate Field Name',
                       '/TM': 'Mapping Name', '/Ff': 'Field Flags', '/V': 'Value', '/DV': 'Default Value'}
        if retval is None:
            retval = OrderedDict()
            catalog = obj.trailer["/Root"]
            if "/AcroForm" in catalog:
                tree = catalog["/AcroForm"]
            else:
                return None
        if tree is None:
            return retval

        obj._checkKids(tree, retval, fileobj)
        for attr in fieldAttributes:
            if attr in tree:
                obj._buildField(tree, retval, fileobj, fieldAttributes)
                break

        if "/Fields" in tree:
            fields = tree["/Fields"]
            for f in fields:
                field = f.getObject()
                obj._buildField(field, retval, fileobj, fieldAttributes)

        return retval

    # This function simply reads the PDF form document and then calls the _getFields function, 
    # and it returns all the fields values (/V) contained within the PDF form file read, as an ordered dictionary
    def get_form_fields(self, infile):
        infile = PdfFileReader(open(infile, 'rb'))
        fields = self._getFields(infile)
        return OrderedDict((k, v.get('/V', '')) for k, v in fields.items())

    # This function simply creates a JavaScript function that is capable of selecting at runtime 
    # the correct drop-down option that for an online form field, that corresponds to the value
    #  contained within the equivalent PDF form field
    def selectListOption(self, all_lines, k, v):
        all_lines.append('function setSelectedIndex(s, v) {')
        all_lines.append('for (var i = 0; i < s.options.length; i++) {')
        all_lines.append('if (s.options[i].text == v) {')
        all_lines.append('s.options[i].selected = true;')
        all_lines.append('return;') 
        all_lines.append('}')
        all_lines.append('}')
        all_lines.append('}')
        all_lines.append('setSelectedIndex(document.getElementById("' + k + '"), "' + v + '");')

    # It is used to read the .ini files, 
    # that have the tags for each selectable, radio-buttons and checkbox fields.
    def readList(self, fname):
        try:
            lst = []
            with open(fname, 'r') as fh:  
                for l in fh:
                    lst.append(l.rstrip(os.linesep))
            return lst
        except BaseException as msg:
            print('read list function... :( ' + str(msg))       


    # Basically, it scans through all of the PDF form fields and generates JavaScript code for each field. 
    # When executed, it will automatically fill in the value of the corresponding online field, 
    # depending on whether the field is a standard field, selectable field, radio-button, or checkbox.
    def createBrowserScript(self, fl, fl_ext, items, pdf_file_name):
        if pdf_file_name and len(fl) > 0:
        # declare .txt file    
            of = os.path.splitext(pdf_file_name)[0] + '.txt'
            all_lines = []
            for k, v in items.items():
                print(k + ' -> ' + v)
                if (v in ['/Yes', '/On']):
                    all_lines.append("document.getElementById('" + k + "').checked = true;\n");
                elif (v in ['/0'] and k in fl_ext):
                    all_lines.append("document.getElementById('" + k + "').checked = true;\n");
                elif (v in ['/No', '/Off', '']):
                    all_lines.append("document.getElementById('" + k + "').checked = false;\n");
                elif (v in [''] and k in fl_ext):
                    all_lines.append("document.getElementById('" + k + "').checked = false;\n");
                elif (k in fl):
                    self.selectListOption(all_lines, k, v)
                else:
                    all_lines.append("document.getElementById('" + k + "').value = '" + v + "';\n");
            # open file of and write contents of ordered dictionary        
            outF = open(of, 'w')
            outF.writelines(all_lines)
            outF.close()

    # Here we use selenium to execute scripts in the browser  
        try:
            driver = webdriver.Chrome()

            # get survey form that was provided earlier
            driver.get(str(self.file_name[0]))

            # write data entry script to this string
            str_list_script = ' '.join(all_lines)
            
            # write alert done script to string
            done_script = "alert('Alert: Data Entered Successfully via selenium !')"

            # Execute data entry javascript file
            driver.execute_script(str_list_script)
            time.sleep(2)

            # generate a alert via javascript
            driver.execute_script(done_script)
            time.sleep(5)

            print("Data Entered Successfully")

        except BaseException as msg:
            print('An error here in selenium occured... :( ' + str(msg))    

    # Executes the rest of the Python script functions that have shown above.
    # It begins by reading the.ini files, after which it can either produce a JavaScript script file (with the.txt extension) 
    # for the name of the PDF form file supplied to the Python script, 
    # or it can build a JavaScript script file for each PDF form document discovered in the same folder
    # as the Python script (with the .txt extension).
    def execute(self, args):
        try: 
            fl = self.readList(str(self.file_name_1[0]))
            fl_ext = self.readList(str(self.file_name_2[0]))
            if len(args) == 2:
                pdf_file_name = args[1]
                items = self.get_form_fields(pdf_file_name)
                self.createBrowserScript(fl, fl_ext, items, pdf_file_name)
            else:
                # add all files that end with .pdf
                files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.pdf')]
                for f in files:
                    items = self.get_form_fields(f)
                    self.createBrowserScript(fl, fl_ext, items, f)
        except BaseException as msg:
            print('An error occured... :( ' + str(msg))    


class FinishScreen(QMainWindow):
    def __init__(self):
            #default instance
            super(FinishScreen, self).__init__()

            #load the UI file
            loadUi("finish.ui",self)

            #define widgets
            self.bt_back = self.findChild(QPushButton, "bt_back")

            #give functionality to button
            self.bt_back.clicked.connect(self.gotoWelcomeScreen)    

            #show the app
            # self.show()

    #go back to the previous menu
    def gotoWelcomeScreen(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)      

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
