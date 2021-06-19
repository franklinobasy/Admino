import sys
import sqlite3 as sql
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QDesktopWidget, QMessageBox
from CBT.properties import *
from CBT.UI import WelcomeLayer, LoginLayer, InstructionLayer
from CBT.tools import loadImage

class CBTApp(QWidget):

    # initialize UI
    def __init__ (self):
        super().__init__()
        self.setObjectName('main')
        logo_filepath = "CBT/images/carina.png"
        self.logo = loadImage(logo_filepath)
        self.logo.setObjectName('image-border')

        self.initializeUI()
    
    def initializeUI(self):
        '''window screen layout'''
        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        desktop = QDesktopWidget().screenGeometry()
        screen_width = desktop.width()
        screen_height = desktop.height()
        x = (screen_width - self.width())/2
        y = (screen_height - self.height())/2
        self.move(x,y)

        '''set the window default layout'''
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        ''' inialize other component '''
        self.loadIntefaces()

        self.show()
    
    def loadIntefaces(self):
        self.welcome_layer = WelcomeLayer()
        self.welcome_layer.load()
        self.welcome_layer.button.clicked.connect(self.showLogin)

        self.login_layer = LoginLayer()
        self.login_layer.load()

        self.instruction_layer = InstructionLayer()
        self.instruction_layer.load()

        self.layout.addWidget(self.logo)
        self.layout.addWidget(self.welcome_layer)

    def closeEvent(self, event):
        quit_msg = QMessageBox.warning(self,"WARNING", "Sorry, You can't exit this test at this moment",
                                QMessageBox.Cancel | QMessageBox.Ok, QMessageBox.Ok)
        if quit_msg == QMessageBox.Ok:
            event.accept() # accept the event  and close the application
        else:
            event.ignore() # ignore the close event
    
    def showLogin(self):
        self.welcome_layer.hide()
        self.layout.addWidget(self.login_layer)
        self.login_layer.login_button.clicked.connect(self.login)

        ''' Using QSqlDatabase'''
        # database = QSqlDatabase.addDatabase("QSQLITE")
        # database.setDatabaseName('database.db')

        # if not database.open():
        #     QMessageBox.critical(
        #                         self,
        #                         "Error!",
        #                         "Database Error: %s" % con.lastError().databaseText(),
        #     )
        #     sys.exit(1)

        '''Using SQLITE3 connection'''
        self.login_conn = sql.connect('database.db')
        
    def login(self):
        # query = QSqlQuery()

        # query.exec_(
        #     '''
        #     SELECT * from accounts
        #     '''
        # )
        data = self.login_conn.execute("SELECT * FROM accounts")

        username = self.login_layer.username_entry.text()
        password = self.login_layer.password_entry.text()
        
        # while query.next():
        #     if (username, password) == (str(query.value(1)), str(query.value(2))):
        #         QMessageBox.information(self,"Login Successful", "You are now logged in!",
        #                         QMessageBox.Cancel | QMessageBox.Ok, QMessageBox.Ok)
        #         self.login_layer.username_entry.clear()
        #         self.login_layer.password_entry.clear()
        #         self.viewInstruction()
        #         break
        # else:
        #     QMessageBox.information(self,"Login Un-Successful", "Oops, try again!",
        #                         QMessageBox.Cancel | QMessageBox.Ok, QMessageBox.Ok)

        for row in data:
            if row[1] == username and row[2] == password:
                QMessageBox.information(self,"Login Successful", "You are now logged in!",
                                 QMessageBox.Cancel | QMessageBox.Ok, QMessageBox.Ok)
                self.login_layer.username_entry.clear()
                self.login_layer.password_entry.clear()
                self.login_conn.close()
                self.viewInstruction()
                break
        else:
            QMessageBox.information(self,"Login Un-Successful", "Oops, try again!",
                                 QMessageBox.Cancel | QMessageBox.Ok, QMessageBox.Ok)
            
    def viewInstruction(self):
        self.logo.hide()
        self.login_layer.hide()
        self.layout.addWidget(self.instruction_layer)
        

    

